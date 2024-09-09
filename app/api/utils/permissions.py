from fastapi import HTTPException, status


def permission_checker(*, permission: str, user):
    print("permission validatio", permission, user)
    # if required_permission not in role_permissions.get(role, []):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Permission denied"
    #     )
    # raise HTTPException(
    #     status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
    # )
