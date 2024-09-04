# def has_permission(required_permission: str):
#     def permission_checker(user: dict = Depends(get_current_user)):
#         role = user["role"]
#         if required_permission not in role_permissions.get(role, []):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Permission denied"
#             )
#     return permission_checker
