from string import Template

create_tbl = Template('''CREATE TABLE IF NOT EXISTS $tbl_name($fields);''')
