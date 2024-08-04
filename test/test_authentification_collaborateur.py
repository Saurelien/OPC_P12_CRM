# import unittest
# from functools import wraps
# from unittest.mock import patch
# from collaborator_app.controller import MainController
# from collaborator_app.model import Collaborator
# from services.utils import Session
#
#
# def authenticate_commercial(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         if Session.user.role == Collaborator.COMMERCIAL:
#             return func(self, *args, **kwargs)
#         else:
#             raise unittest.SkipTest("Role Commercial requis")
#     return wrapper
#
#
# def authenticate_support(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         if Session.user.role == Collaborator.SUPPORT:
#             return func(self, *args, **kwargs)
#         else:
#             raise unittest.SkipTest("Role Support requis")
#     return wrapper
#
#
# def authenticate_gestion(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         if Session.user.role == Collaborator.GESTION:
#             return func(self, *args, **kwargs)
#         else:
#             raise unittest.SkipTest("Role Gestion requis")
#     return wrapper
#
#
# class TestCollaboratorLogin(unittest.TestCase):
#     def test_commercial_login(self):
#         Session.logout()
#         print("user role:", Session.user)
#         user = unittest.mock.Mock(spec=Collaborator, role=Collaborator.COMMERCIAL)
#         Session.login(user)
#         print("user role after login:", Session.user.role)
#         MainController.display_role_menu(Collaborator.COMMERCIAL)
#         print("Finished test_commercial_login")
#
#     def test_support_login(self):
#         Session.logout()
#         print("user role:", Session.user.role)
#         user = unittest.mock.Mock(spec=Collaborator, role=Collaborator.SUPPORT)
#         Session.login(user)
#         print("user role after login:", Session.user.role)
#         MainController.display_role_menu(Collaborator.SUPPORT)
#         print("Finished test_support_login")
#
#     def test_management_login(self):
#         Session.logout()
#         print("user role:", Session.user.role)
#         user = unittest.mock.Mock(spec=Collaborator, role=Collaborator.GESTION)
#         Session.login(user)
#         print("user role after login:", Session.user.role)
#         MainController.display_role_menu(Collaborator.GESTION)
#         print("Finished test_management_login")
