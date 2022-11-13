def set_new_csrf_token(action_url):
    path = './endpoints.yml'
    f = open(path, 'r')
    linelist = f.readlines()
    f.close

    # Re-open file here
    f2 = open(path, 'w')
    is_start = False
    for line in linelist:
        if line.strip() == '# End':
           is_start = False  
        if is_start:
           key_name,value_config = line.split(': "')
           if key_name.strip() == 'url':
              line = '  url: "' + action_url+'" \n'
        #    line = line.replace('Miko', 'new')
        if line.strip() == 'action_endpoint:':
            is_start = True
        f2.write(line)

    f2.close()