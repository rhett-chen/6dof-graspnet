import os

grasps_path = 'F:/research/Liu/relevant_projects/dataset/unified_grasp_data/grasps'
meshes_path = 'F:/research/Liu/relevant_projects/dataset/unified_grasp_data/meshes'
name_mapping = {'Bottle': '02876657', 'Bowl': '02880940', 'mug': '03797390'}
url = 'http://shapenet.cs.stanford.edu/shapenet/obj-zip/ShapeNetCore.v2/'
txt = open('shapeid.txt', 'w')
success_num = 0
total_num = 0

for obj in os.listdir(grasps_path):
    total_num += 1
    obj_category = obj.split('_')[0]
    if obj_category in ['box', 'cylinder']:
        continue
    shape_net_id = obj.split('_')[1]
    final_url = url + name_mapping[obj_category] + '/' + shape_net_id + '/models' + '/model_normalized.obj'
    target_path = meshes_path + '/' + obj_category + '/' + shape_net_id + '.obj'
    os.system('wget ' + final_url + ' -O ' + target_path)
    if os.path.getsize(meshes_path + '/' + obj_category + '/' + shape_net_id + '.obj') < 5:
        txt.write(obj_category + ' ' + shape_net_id + '\n')
        txt.flush()
        os.remove(meshes_path + '/' + obj_category + '/' + shape_net_id + '.obj')
    else:
        success_num += 1
print('total num: ', total_num)
print('success: ', success_num)
print('failure num: ', total_num - success_num)
