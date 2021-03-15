import os

meshes_path = '/home/share2/zibo/unified_grasp_data/meshes/'
manifold_command = '/home/share2/zibo/Manifold/build/manifold '
simplify_command = '/home/share2/zibo/Manifold/build/simplify '
txt = open('id.txt', 'w')
for category in ['Bottle', 'Bowl', 'mug']:
    original_obj_path = os.path.join(meshes_path, category + '_o')
    # for obj_name in os.listdir(original_obj_path):
    #     command = manifold_command + os.path.join(original_obj_path, obj_name) + ' temp.watertight.obj -s'
    #     print(command)
    #     os.system(command)
    #     command = simplify_command + ' -i temp.watertight.obj -o ' + os.path.join(meshes_path, category, obj_name) + \
    #               ' -m -r 0.02'
    #     print(command)
    #     os.system(command)

    new_obj_path = os.path.join(meshes_path, category)
    new_objs = os.listdir(new_obj_path)
    old_objs = os.listdir(original_obj_path)
    print(category + ':  old num = ', len(old_objs))
    print(category + ':  new num = ', len(new_objs))
    print(category + ':  lack num = ', len(old_objs) - len(new_objs))
    for obj in old_objs:
        if obj in new_objs:
            continue
        else:
            txt.write(category + ' ' + obj + '\n')
