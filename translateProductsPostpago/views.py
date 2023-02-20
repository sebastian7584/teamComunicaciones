from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import TranslateProductSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
from .models import TranslateProductPostpago
import json
from azureControl.azureControl import Azure_db
from sqlControl.sqlControl import Sql_conexion
import numpy as np
db = Azure_db()


@api_view(["GET", "POST","DELETE", "PUT"])
def adminProductPostpagoView(request):

    if request.method =="POST":
        equipo = request.data['equipo']
        stok = request.data['stok']
        iva = request.data['iva']
        active = request.data['active']
        data = {'id':equipo,'stok':stok,'iva':iva,'active':active}

        if active == '1':
            query= (
                "SELECT TOP(1000) P.Nombre, lPre.nombre, ValorBruto "  
                "FROM dbo.ldpProductosXAsociaciones lProd " 
                "JOIN dbo.ldpListadePrecios  lPre ON lProd.ListaDePrecios = lPre.Codigo " 
                "JOIN dbo.Productos  P ON lProd.Producto = P.Codigo " 
                "JOIN dbo.TiposDeProducto  TP ON P.TipoDeProducto = TP.Codigo " 
                f"WHERE TP.Nombre = 'Postpago' and P.Visible = 1 and P.Nombre = '{stok}';"
            )
            conexion = Sql_conexion(query)
            data = conexion.get_data()
            # data = np.asarray(data)
            if len(data)==0:
                raise AuthenticationFailed('Producto inexistente en Stok')
            
            listaStok = []
            for dato in data:
                nombreStok = dato[0]
                if nombreStok not in listaStok:
                    listaStok.append(nombreStok)
            for nstok in listaStok:
                validacion = nstok == stok
                if validacion == False:
                    raise AuthenticationFailed(f'intente usar {nstok} y no {stok}')
        
        try:
            db.create_item('traduccion_equipos_postpago', data)
        except:
            raise AuthenticationFailed('Error Creando Traduccion')

        return Response(data)

      

    if request.method == "GET":
        data = db.read_items('traduccion_equipos_postpago')
        return Response(data)
    
    if request.method == "DELETE":
        translate = TranslateProductPostpago.objects.filter(id='1').first()
        serializer = TranslateProductSerializer(translate)
        translate.delete()
        return Response({'s':'s'})
    
    if request.method == "PUT":
        equipo = request.data['equipo']
        stok = request.data['stok']
        iva = request.data['iva']
        active = request.data['active']
        data = db.read_item('traduccion_equipos_postpago',equipo)
        data['stok'] = stok
        data['iva']=iva
        data['active']=active
        db.replace_item('traduccion_equipos_postpago',data)

@api_view(["POST"])
def translateProductPostpagoView(request):
    if request.method == "POST":
        data = request.body
        data = json.loads(data)
        translates = db.read_items('traduccion_equipos_postpago')
        crear =[]
        newData = []
        lista=[]
        traductor = {}
        validate = True
        for i in translates:
            traductor[i['id']] = i
        for i in range (len(data)):
            nombre = data[i][0]
            try:
                nombre2 = traductor[nombre]['stok']
                costo = data[i][1]
                cliente0A5MesesSinIva = data[i][2]
                cliente6A23MesesSinIva = data[i][3]
                clienteMayorA24MesesSinIva = data[i][4]
                
                data[i][0] = nombre2
                if traductor[nombre]['active'] == '1' and nombre2 not in lista:
                    if validate:
                        lista.append(nombre2)
                        updatePrices = UpdatePrices(
                        nombre2,
                        costo,
                        cliente0A5MesesSinIva,
                        cliente6A23MesesSinIva,
                        clienteMayorA24MesesSinIva,
                        traductor[nombre]['iva'])
                        newData.append(updatePrices.returnData())
            except KeyError:
                crear.append([data[i][0]])
                validate = False
        if validate:
            dataResponse = newData
        else:
            dataResponse = crear
        response = {'validate': validate, 'data':dataResponse }

        return Response(response)

class UpdatePrices:

    def __init__(
        self, 
        producto,
        costo,
        cliente0A5MesesSinIva,
        cliente6A23MesesSinIva,
        clienteMayorA24MesesSinIva,
        iva
        ):
        

        self.producto = producto
        self.iva = iva
        self.costoActual = costo - 2000
        self.precioPubicoSinIva = '999999999.00'
        self.subdistribuidorSinIva = '999999999.00'
        self.freeMobileStore = '999999999.00'
        self.cliente0A5MesesSinIva = cliente0A5MesesSinIva
        self.cliente6A23MesesSinIva = cliente6A23MesesSinIva
        self.clienteMayorA24MesesSinIva = clienteMayorA24MesesSinIva
        self.clienteDescuentoKitPrepagoSinIva = '999999999.00'
        self.distritadosSinIva = '999999999.00'
        self.premiumSinIva = '999999999.00'
        self.tramitarSinIva = '999999999.00'
        self.peopleSinIva = '999999999.00'
        self.cooservunalSinIva = '999999999.00'
        self.fintechOficinasTeamSinIva = '999999999.00'
        self.fintechZonificacionSinIva = '999999999.00'
        self.oficinaMovilSinIva = '999999999.00'
        self.elianaRodas = '999999999.00'

    def formatoData(self):
        if (type(self.producto)) == float : self.producto  = round(self.producto ,2)
        if (type(self.costoActual)) == float : self.costoActual  = round(self.costoActual ,2)
        if (type(self.precioPubicoSinIva)) == float : self.precioPubicoSinIva  = round(self.precioPubicoSinIva ,2)
        if (type(self.subdistribuidorSinIva)) == float : self.subdistribuidorSinIva  = round(self.subdistribuidorSinIva ,2)
        if (type(self.freeMobileStore)) == float : self.freeMobileStore  = round(self.freeMobileStore ,2)
        if (type(self.cliente0A5MesesSinIva)) == float : self.cliente0A5MesesSinIva  = round(self.cliente0A5MesesSinIva ,2)
        if (type(self.cliente6A23MesesSinIva)) == float : self.cliente6A23MesesSinIva  = round(self.cliente6A23MesesSinIva ,2)
        if (type(self.clienteMayorA24MesesSinIva)) == float : self.clienteMayorA24MesesSinIva  = round(self.clienteMayorA24MesesSinIva ,2)
        if (type(self.clienteDescuentoKitPrepagoSinIva)) == float : self.clienteDescuentoKitPrepagoSinIva  = round(self.clienteDescuentoKitPrepagoSinIva ,2)
        if (type(self.distritadosSinIva)) == float : self.distritadosSinIva  = round(self.distritadosSinIva ,2)
        if (type(self.premiumSinIva)) == float : self.premiumSinIva  = round(self.premiumSinIva ,2)
        if (type(self.tramitarSinIva)) == float : self.tramitarSinIva = round(self.tramitarSinIva,2)
        if (type(self.peopleSinIva)) == float : self.peopleSinIva  = round(self.peopleSinIva ,2)
        if (type(self.cooservunalSinIva)) == float : self.cooservunalSinIva  = round(self.cooservunalSinIva ,2)
        if (type(self.fintechOficinasTeamSinIva)) == float : self.fintechOficinasTeamSinIva  = round(self.fintechOficinasTeamSinIva ,2)
        if (type(self.fintechZonificacionSinIva)) == float : self.fintechZonificacionSinIva  = round(self.fintechZonificacionSinIva ,2)
        if (type(self.oficinaMovilSinIva)) == float : self.oficinaMovilSinIva  = round(self.oficinaMovilSinIva ,2)
        if (type(self.elianaRodas)) == float : self.elianaRodas  = round(self.elianaRodas ,2)
    
    def returnData(self):
        self.formatoData()
        return [
            str(self.producto),
            str(self.costoActual),
            str(self.precioPubicoSinIva),
            str(self.subdistribuidorSinIva),
            str(self.freeMobileStore),
            str(self.cliente0A5MesesSinIva),
            str(self.cliente6A23MesesSinIva),
            str(self.clienteMayorA24MesesSinIva),
            str(self.clienteDescuentoKitPrepagoSinIva),
            str(self.distritadosSinIva),
            str(self.premiumSinIva),
            str(self.tramitarSinIva),
            str(self.peopleSinIva),
            str(self.cooservunalSinIva),
            str(self.fintechOficinasTeamSinIva),
            str(self.fintechZonificacionSinIva),
            str(self.oficinaMovilSinIva),
            str(self.elianaRodas),
            ]
