ROLES = "Roles"
USERS = "Usuarios"
PAYMENTS = "Pagos"
DASHBOARD_POC = "Dashboard punto de recaudo"
CLIENTS = "Clientes"
DASHBOARD = "Dashboard"
SHOPPING = "Compras"


def generate_menu(items: list):
    return [{"name": item} for item in items]


SUPER_ADMIN_MENU = generate_menu(
    [ROLES, USERS, PAYMENTS, DASHBOARD_POC, CLIENTS, DASHBOARD, SHOPPING]
)
ADMIN_MENU = generate_menu([ROLES, USERS, PAYMENTS, DASHBOARD_POC, CLIENTS])
CLIENT_MENU = generate_menu([DASHBOARD, SHOPPING, PAYMENTS])
