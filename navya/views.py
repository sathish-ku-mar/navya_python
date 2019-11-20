# Create your views here.
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.http.request import QueryDict
from .settings import global_file_path
import json


def read_file(path, mode='r'):
    with open(path, mode) as json_file:
        data = json.load(json_file)
        return data


def write_file(path, data, mode='w'):
    with open(path, mode) as json_file:
        json.dump(data, json_file)
        return True


def get_user(id):
    path = global_file_path + '/data_store/user.json'
    data = read_file(path)
    return [i for i in data if str(i['id']) == str(id)][0]


def get_role(data):
    path = global_file_path + '/data_store/roles.json'
    file_data = read_file(path)
    return [i for i in file_data if i['id'] in data]


def get_permissions(data):
    path = global_file_path + '/data_store/permissions.json'
    file_data = read_file(path)
    return [i for i in file_data if i['id'] in data]


def modify_role(id, per):
    path = global_file_path + '/data_store/roles.json'
    data = read_file(path)

    for key, value in enumerate(data):
        if value['id'] == id:
            data[key]['permissions'] = per

    return write_file(path, data, mode='w')


def delete_permissions(id):
    path = global_file_path + '/data_store/permissions.json'
    data = read_file(path)

    for key, value in enumerate(data):
        if value['id'] == id:
            data.pop(key)

    return write_file(path, data, mode='w')


class UserViewSet(viewsets.ModelViewSet):
    """
        A simple ViewSet for the User's.
    """

    def get_user_permissions(self, request, id):
        """
            To get the User permissions list
            URL Structure: /user/user1/
            Required Fields: id
        """
        user = get_user(id)
        role = get_role(user['roles'])
        flat_list = [item for sublist in role for item in sublist['permissions']]
        permissions = get_permissions(flat_list)
        return Response(permissions)

    def get_checkpermission(self, request):
        """
            To check user has permissions based on the permission id
            URL Structure: /checkpermission/?userid=user1&permissionid=perm6
            Required Fields: userid, permissionid
        """
        user_id = request.GET['userid']
        permissionid = request.GET['permissionid']

        user = get_user(user_id)
        role = get_role(user['roles'])
        flat_list = [item for sublist in role for item in sublist['permissions'] if permissionid == item]
        permissions = True if flat_list else False
        return Response(permissions)

    def modify_permissions_of_role(self, request, roleid):
        """
            To modify the permissions of the Role
            URL Structure: /roles/role3/
            Required Fields: roleid
        """

        res = modify_role(roleid, request.data['permissions'])
        return Response(res)

    def delete_permission (self, request, permission_id):
        """
            To delete the permission based on the permission id
            URL Structure: /permissions/perm6/
            Required Fields: permission_id
        """

        res = delete_permissions(permission_id)
        return Response(res)