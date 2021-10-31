import pandas as pd
import re


class ERD:
    __start_of_file = """@startuml
' hide the spot
 hide circle

' avoid problems with angled crows feet
skinparam linetype ortho

' Create the entities"""
    __end_of_file = '@enduml'

    __relationship_dict = {
        'left' : {
            '[0:1]': '|o',
            '[1:1]': '||',
            '[0:M]': '}o',
            '[1:M]': '}|'
        },
        'right' : {
            '[0:1]': 'o|',
            '[1:1]': '||',
            '[0:M]': 'o{',
            '[1:M]': '|{'
        }
    }

    def __init__(self, entity_file: str):
        self.__entity_file: pd.ExcelFile = pd.ExcelFile(entity_file)
        self.__entities = self.__get_attributes()
        self.__relationships = self.__get_relationships()

    def __get_attributes(self) -> list:
        '''
        Parse the entities from the entity file
        :return: a list of worksheet names for the entities
        '''
        return self.__entity_file.sheet_names[:-1]

    def __get_relationships(self) -> str:
        '''
        Parse the relationships from the entity file.

        NOTE: This program assumes the 'relationships' worksheet goes LAST in the workbook
        :return: the name of relationship worksheet
        '''
        return self.__entity_file.sheet_names[-1]

    def __generate_relationships(self) -> str:
        '''
        Generate relationships based on those noted in the Excel file.

        NOTE: Requires a worksheet named "relationships" to be at the END of the
        workbook. This notation uses [M:N] syntax.
        :return: a string denoting the relationships between entities
        '''

        relationship_str = "' Create the relationships\n"
        # Open the "relationships" worksheet
        sheet_name = 'relationships'
        df = pd.read_excel(self.__entity_file, sheet_name=sheet_name)
        for index, row in df.iterrows():
            left = row.Left.lower()
            right = row.Right.lower()
            l_rel = row.L_Relationship
            r_rel = row.R_Relationship

            relationship_str += f"{left} {self.__relationship_dict['left'][l_rel]}"
            relationship_str += '--'
            relationship_str += f"{self.__relationship_dict['right'][r_rel]} {right}\n"

        return relationship_str

    def generate(self):
        out_file = 'ERD.puml'
        print(f'[*] Generating {out_file}...')
        with open(out_file, 'w') as file:
            file.write(f'{self.__start_of_file}\n')
            # Parse through the worksheets (entity names)
            for worksheet in self.__entities:
                entity = worksheet
                # Check if we have a subclass
                pattern = r'(?<=\()\w+(?=\))'
                regex = re.compile(pattern)
                subclass = regex.findall(worksheet)
                # Rename the worksheet (entity) if there is a subclass
                if subclass:
                    entity = entity.replace(f'({subclass[0]})', '').strip()
                # Initialize the template
                template = f"entity \"{entity}\" as {entity.lower()}{f' extends {subclass[0].lower()}' if subclass else ''} {{\n"
                # Create a DataFrame
                df = pd.read_excel(self.__entity_file, sheet_name=worksheet)

                # Get a count of the primary/foreign keys
                key_count = 0
                df.Key.fillna('none', inplace=True)
                for cell in df.Key:
                    key_count += 1 if cell.upper() in ['PRIMARY', 'FOREIGN'] else 0

                # Iterate through each row (attribute) of the DataFrame
                for index, row in df.iterrows():
                    attribute = row.Attribute
                    key = row.Key
                    if key in ['PRIMARY', 'FOREIGN', 'REQUIRED']:
                        attribute = f'* {attribute}'
                    template += f"\t{attribute}\
{f' <<PK>>' if key == 'PRIMARY' else ' <<FK>>' if key == 'FOREIGN' else ''}\n"
                    if key_count and index == key_count - 1:
                        template += '\t--\n'
                template += '}\n\n'

                file.write(template)

            # Write the relationships
            relationships = self.__generate_relationships()

            file.write(relationships)

            file.write(f'{self.__end_of_file}')

            print('[*] Done')
