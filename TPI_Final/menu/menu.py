from models.role import role


class Menu():

    @classmethod
    def MenuesStatic(self, idrole):
        rol = role.query.get(idrole)
        if ("Admin").lower()== rol.name.lower():       
            return  OptionMenu.GetAdmin()
        elif ("User").lower()== rol.name.lower():
            return OptionMenu.GetEmployees()  # Ver si redirigir a otra  pagina
        else:
            return OptionMenu.GetPartners() 
    
class OptionMenu():
    def GetAdmin():
        menunav=[
        {
            "url":"/kayak",
            "displayName":"Kayak",
            "active":"active kayak",
            "isSubMenu": "false"
        },
        {
            "url":"/user",
            "displayName":"Usuario",
            "active":"user",
            "isSubMenu": "false"
        },
        {
            "url":"/hangers",
            "displayName":"Parches",
            "active":"hanger",
            "isSubMenu": "false"
        },
        {
            "url":"/kayaktypes",
            "displayName":"Tipo kayak",
            "active":"hanger",
            "isSubMenu": "false"
        },
        {
            "url":"/locations",
            "displayName":"Ubicacion",
            "active":"partner",
            "isSubMenu": "false"
        },
        {
            "url":"/calendarYear",
            "displayName":"Calendario",
            "active":"partner",
            "isSubMenu": "false"
        },
        {
            "url":"/payment",
            "displayName":" Cobranza",
            "active":"hanger",
            "isSubMenu": "false"
        },
        {
            "displayName":"Informes",
            "isSubMenu": "true",
            "Submenu":[
                 {
                    "url":"/paymenteMonth",
                    "displayName":"Informa mess",
                    "active":"partner",
                    "isSubMenu": "false"
                },
                {
                    "url":"/ritired",
                    "displayName":"Kayak",
                    "active":"partner",
                    "isSubMenu": "false"
                },
                {
                    "url":"/ejemplo",
                    "displayName":"ejemplo",
                    "active":"partner",
                    "isSubMenu": "false"
                }
            ]
        },
        {
            "url":"",
            "displayName":"",
            "active":"",
            "isSubMenu": "false"
        }
        ]
        return menunav

    def GetEmployees():
        menunav=[
            {
                "url":"/Kayak",
                "displayName":"Crear kayak",
                "active":"active kayak"
            },
            {
                "url":"/User",
                "displayName":"Crear usuario",
                "active":"user"
            },
            {
                "url":"/Hanger",
                "displayName":" Crear parches",
                "active":"hanger"
            },
            {
                "url":"/payment",
                "displayName":" Cobranza",
                "active":"hanger"
            }
            # ,
            # {
            #     "url":"/Location",
            #     "displayName":"Crear ubicacion",
            #     "active":"partner"
            # }
        ]
        return menunav;
    
    def GetPartners():
        menunav=[
            {
                "url":"/user",
                "displayName":"Historial kayak",
                "active":"active kayak"
            },
            {
                "url":"/user",
                "displayName":"Historial de pago",
                "active":"user"
            },
            {
                "url":"/user",
                "displayName":"Seleccionar Kayak",
                "active":"hanger"
            }
            # ,
            # {
            #     "url":"/Browser/Location",
            #     "displayName":"Crear ubicacion",
            #     "active":"partner"
            # }
        ]
        return menunav;
  