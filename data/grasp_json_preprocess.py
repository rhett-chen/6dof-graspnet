import json
import os
import copy
from shutil import copyfile

original_json_path = '/home/share2/zibo/unified_grasp_data/grasps'
new_json_path = '/home/share2/zibo/unified_grasp_data/new_grasps'
meshes_path = '/home/share2/zibo/unified_grasp_data/'
categories = ['Bottle', 'Bowl', 'box', 'cylinder', 'mug']

# print(len(os.listdir(original_json_path)))
# mesh_num = 0
# for i in categories:
#     mesh_num += len(os.listdir(os.path.join(meshes_path, i)))
# print(mesh_num)
count_valid = 0
count_changed = 0
count_error = 0
for json_name in os.listdir(original_json_path):
    json_file_path = os.path.join(original_json_path, json_name)
    print(json_file_path)
    temp_data = json.load((open(json_file_path, 'r')))
    # print('cad path: ', temp_data['cad_path'])
    print('object: ', temp_data['object'])
    if os.path.exists(os.path.join(meshes_path, temp_data['object'])):
        copyfile(json_file_path, os.path.join(new_json_path, json_name))
        print(temp_data['object'] + ' exist, already copied to new dir')
        count_valid += 1
    else:
        if temp_data['object'].split('.')[-1] == 'stl':
            obj_stl_path = temp_data['object'].split('.')[0] + '.obj'
        elif temp_data['object'].split('.')[-1] == 'obj':
            obj_stl_path = temp_data['object'].split('.')[0] + '.stl'
        if os.path.exists(os.path.join(meshes_path, obj_stl_path)):
            print(temp_data['object'] + ' does not exists, ' + obj_stl_path + ' exists, already saved to new dir')
            new_json_file = copy.deepcopy(temp_data)
            new_json_file['object'] = obj_stl_path
            # new_json_file['cad_path'] = 'unified_grasp_data/' + obj_stl_path
            json.dump(new_json_file, open(os.path.join(new_json_path, json_name), 'w'))
            count_changed += 1
            # print('cad path: ', new_json_file['cad_path'])
            print('object: ', new_json_file['object'])
        else:
            print(temp_data['object'] + ' and ' + obj_stl_path + ' both dont exist')
            count_error += 1
    print('\n')

print('already exist num: ', count_valid)
print('exits after changing name num: ', count_changed)
print('doesnt exists num: ', count_error)
