from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import TranslateProductSerializer
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from .models import TranslateProduct
import json
from azureControl.azureControl import Azure_db
db = Azure_db()


@api_view(["GET", "POST","DELETE"])
def adminProductView(request):

    if request.method =="POST":
        equipo = request.data['equipo']
        stok = request.data['stok']
        iva = request.data['iva']
        active = request.data['active']
        data = {'id':equipo,'stok':stok,'iva':iva,'active':active}
        print(data)
        try:
            db.create_item('traduccion_equipos_prepago', data)
        except:
            raise AuthenticationFailed('Error')

        return Response(data)

    if request.method == "GET":
        data = db.read_items('traduccion_equipos_prepago')
        return Response(data)
    
    if request.method == "DELETE":
        translate = TranslateProduct.objects.filter(id='21').first()
        serializer = TranslateProductSerializer(translate)
        translate.delete()
        return Response({'s':'s'})

@api_view(["POST"])
def translateProductView(request):
    if request.method == "POST":
        data = request.body
        data = json.loads(data)
        translates = db.read_items('traduccion_equipos_prepago')
        crear =[]
        newData = []
        lista=[]
        traductor = {}
        validate = True
        for i in translates:
            traductor[i['id']] = i
        print(traductor)

        for i in range (len(data)):
            nombre = data[i][0]
            try:
                nombre2 = traductor[nombre]['stok']
                precioConIva = data[i][1]
                descuentoClaroPagoContado = data[i][2]
                valorSinIvaConDescuento = data[i][3]
                valorPagarDescuentoContado = data[i][4]
                descuentoAlDistribuidor = data[i][5]
                precioVtaDistribuidorSinIva = data[i][6]
                precioVtaDistribuidorConIva = data[i][7]
                data[i][0] = nombre2
                if traductor[nombre]['active'] == '1' and nombre2 not in lista:
                    if validate:
                        lista.append(nombre2)
                        updatePrices = UpdatePrices(
                        nombre2,
                        precioConIva,
                        descuentoClaroPagoContado,
                        valorSinIvaConDescuento,
                        valorPagarDescuentoContado,
                        descuentoAlDistribuidor,
                        precioVtaDistribuidorSinIva,
                        precioVtaDistribuidorConIva,
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
        precioConIva,
        descuentoClaroPagoContado,
        valorSinIvaConDescuento,
        valorPagarDescuentoContado,
        descuentoAlDistribuidor,
        precioVtaDistribuidorSinIva,
        precioVtaDistribuidorConIva,
        iva
        ):
        

        self.producto = producto
        self.precioConIva = precioConIva
        self.descuentoClaroPagoContado = descuentoClaroPagoContado
        self.valorSinIvaConDescuento = valorSinIvaConDescuento
        self.valorPagarDescuentoContado = valorPagarDescuentoContado
        self.descuentoAlDistribuidor = descuentoAlDistribuidor
        self.precioVtaDistribuidorSinIva = precioVtaDistribuidorSinIva
        self.precioVtaDistribuidorConIva = precioVtaDistribuidorConIva
        self.iva = iva
        self.costoActual = '999999999.00'
        self.precioPubicoSinIva = '999999999.00'
        self.subdistribuidorSinIva = '999999999.00'
        self.freeMobileStore = '999999999.00'
        self.cliente0A5MesesSinIva = '999999999.00'
        self.cliente6A23MesesSinIva = '999999999.00'
        self.clienteMayorA24MesesSinIva = '999999999.00'
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
        self.newcostoActual()
        self.newprecioPubicoSinIva()
        self.newsubdistribuidorSinIva()
        self.newfreeMobileStore()
        self.newcliente0A5MesesSinIva()
        self.newcliente6A23MesesSinIva()
        self.newclienteMayorA24MesesSinIva()
        self.newclienteDescuentoKitPrepagoSinIva()
        self.newdistritadosSinIva()
        self.newpremiumSinIva()
        self.newtramitarSinIva()
        self.newpeopleSinIva()
        self.newcooservunalSinIva()
        self.newfintechOficinasTeamSinIva()
        self.newfintechZonificacionSinIva()
        self.newoficinaMovilSinIva()
        self.newelianaRodas()

    def newcostoActual(self):
        self.costoActual = self.precioVtaDistribuidorSinIva - 2000

    def newprecioPubicoSinIva(self):
        if self.descuentoClaroPagoContado >0:
            descuento = 2000
        else:
            descuento = 0
        self.precioPubicoConIva= self.valorPagarDescuentoContado + descuento
        if self.iva == '1':
            self.precioPubicoSinIva = (self.precioPubicoConIva - 2380) / 1.19
        else:
            self.precioPubicoSinIva = (self.precioPubicoConIva - 2380)

    def newsubdistribuidorSinIva(self):
        precioSimEquipoSinIva = self.precioPubicoSinIva + 2000
        psqsi = precioSimEquipoSinIva
        self.psqsi = psqsi
        # Sub Descuento

        if psqsi > 702000:
            subDescuento = 38127
        elif psqsi > 520000:
            subDescuento = 35360
        elif psqsi > 442000:
            subDescuento = 31200
        elif psqsi > 299000:
            subDescuento = 27727
        elif psqsi > 130000:
            subDescuento = 24274
        elif psqsi > 104000:
            subDescuento = 17327
        elif psqsi > 91000:
            subDescuento = 13874
        elif psqsi > 78000:
            subDescuento = 10400
        elif psqsi > 51948:
            subDescuento = 7280
        elif psqsi > 18200:
            subDescuento = 4160
        else:
            subDescuento = 0

        # Descuento Adicional Sub
        if psqsi > 2500000:
            descuentoAdicionalSub = 25410
        elif psqsi > 1500000:
            descuentoAdicionalSub = 20510
        elif psqsi > 702001:
            descuentoAdicionalSub = 28210
        elif psqsi > 522001:
            descuentoAdicionalSub = 14560
        elif psqsi > 442001:
            descuentoAdicionalSub = 12600
        elif psqsi > 299001:
            descuentoAdicionalSub = 10780
        elif psqsi > 130001:
            descuentoAdicionalSub = 1890
        else:
            descuentoAdicionalSub = 0
        
        self.descuentoAdicionalsub = descuentoAdicionalSub
        
        if self.iva == '1':
            totalDecuentos = subDescuento + (descuentoAdicionalSub/1.19)
            subPrecioSinIva = psqsi - totalDecuentos +500
            subPrecioConIva = subPrecioSinIva * 1.19
            self.subdistribuidorSinIva = (subPrecioConIva-2380) / 1.19
        else:
            totalDecuentos = subDescuento + descuentoAdicionalSub
            subPrecioSinIva = psqsi - totalDecuentos +500
            subPrecioConIva = subPrecioSinIva + 380
            self.subdistribuidorSinIva = (subPrecioConIva - 2380)
        

    def newfreeMobileStore(self):
        # Ya no se utiliza, alianza vieja
        pass

    def newcliente0A5MesesSinIva(self):
        # Para postpago
        pass

    def newcliente6A23MesesSinIva(self):
        # Para postpago
        pass

    def newclienteMayorA24MesesSinIva(self):
        # Para postpago
        pass

    def newclienteDescuentoKitPrepagoSinIva(self):
        if self.descuentoClaroPagoContado > 0:
            if self.iva == '1':
                self.clienteDescuentoKitPrepagoSinIva = (self.precioConIva / 1.19) + 1680
            else:
                self.clienteDescuentoKitPrepagoSinIva =self.precioConIva - 2380 +2000
        else:
            self.clienteDescuentoKitPrepagoSinIva = self.precioPubicoSinIva

    def newdistritadosSinIva(self):
        # Ya no se utiliza, alianza vieja
        pass

    def newpremiumSinIva(self):

        # Descuento Premium

        if self.psqsi > 702000:
            descuentoPremium = 40040
        elif self.psqsi > 522000:
            descuentoPremium = 37655
        elif self.psqsi > 442000:
            descuentoPremium = 34069
        elif self.psqsi > 299000:
            descuentoPremium = 31075
        elif self.psqsi > 130000:
            descuentoPremium = 28098
        elif self.psqsi > 104000:
            descuentoPremium = 21658
        elif self.psqsi > 91000:
            descuentoPremium = 17342
        elif self.psqsi > 78000:
            descuentoPremium = 13000
        elif self.psqsi > 51948:
            descuentoPremium = 9100
        elif self.psqsi > 18200:
            descuentoPremium = 5200
        else:
            descuentoPremium = 0
        
        if self.iva == '1':
            totalDescuento = descuentoPremium + (self.descuentoAdicionalsub/1.19)
            elianaPrecioSinIva = self.psqsi - totalDescuento
            elianaPrecioConIVa = elianaPrecioSinIva * 1.19
            self.premiumSinIva = (elianaPrecioConIVa - 2380) / 1.19

        else:
            totalDescuento = descuentoPremium + self.descuentoAdicionalsub
            elianaPrecioConIVa = self.precioPubicoSinIva + 2000 - totalDescuento +380
            self.premiumSinIva = elianaPrecioConIVa - 2380
        
    def newtramitarSinIva(self):
        if self.psqsi > 702000:
            descuentoTramitar = 38127
        elif self.psqsi > 522000:
            descuentoTramitar = 35360
        elif self.psqsi > 442000:
            descuentoTramitar = 31200
        elif self.psqsi > 299000:
            descuentoTramitar = 27727
        elif self.psqsi > 130000:
            descuentoTramitar = 24274
        elif self.psqsi > 104000:
            descuentoTramitar = 17327
        elif self.psqsi > 91000:
            descuentoTramitar = 13874
        elif self.psqsi > 78000:
            descuentoTramitar = 10400
        elif self.psqsi > 51948:
            descuentoTramitar = 7280
        elif self.psqsi > 18200:
            descuentoTramitar = 4160
        else:
            descuentoTramitar = 0
        
        

        if self.iva == '1':
            tramitarSinIva = self.psqsi - descuentoTramitar
            tramitarConIVa = tramitarSinIva * 1.19
            self.tramitarSinIva = (tramitarConIVa - 2380) / 1.19 + 4201.68
        else:
            tramitarConIVa = self.psqsi - descuentoTramitar +380
            self.tramitarSinIva = (tramitarConIVa - 2380) + 5000

    def newpeopleSinIva(self):
        if self.iva == '1':
            peopleConIVa = self.precioPubicoConIva * 1.05
            self.peopleSinIva = (peopleConIVa - 2380) / 1.19

        else:
            peopleConIVa = self.precioPubicoSinIva * 1.05
            # 933064 es la base del iva, cualquier cambio en base mover aca
            baseIva = 933064

            if peopleConIVa > baseIva:
                self.peopleSinIva = baseIva
            else:
                self.peopleSinIva = peopleConIVa

    def newcooservunalSinIva(self):
        # Ya no se utiliza, alianza vieja
        pass

    def newfintechOficinasTeamSinIva(self):
        if self.iva == '1':
            self.fintechOficinasTeamSinIva = (self.precioPubicoConIva + 60000 - 2380) / 1.19
        else:
            # 933064 es la base del iva, cualquier cambio en base mover aca
            baseIva = 933064
            self.fintechOficinasTeamSinIva = (self.precioPubicoConIva + 60000 - 2380)
            if self.fintechOficinasTeamSinIva > baseIva:
                self.fintechOficinasTeamSinIva = baseIva

    def newfintechZonificacionSinIva(self):
        if self.iva == '1':
            self.fintechZonificacionSinIva = (self.precioPubicoConIva + 80000 - 2380) / 1.19
        else:
            # 933064 es la base del iva, cualquier cambio en base mover aca
            baseIva = 933064 
            self.fintechZonificacionSinIva = (self.precioPubicoConIva + 80000 - 2380)
            if self.fintechZonificacionSinIva > baseIva:
                self.fintechZonificacionSinIva = baseIva

    def newoficinaMovilSinIva(self):
        if self.descuentoClaroPagoContado > 0:
            self.oficinaMovilSinIva = self.precioPubicoSinIva
        else:
            self.oficinaMovilSinIva = self.subdistribuidorSinIva

    def newelianaRodas(self):
        # Ya no se utiliza, alianza vieja
        pass

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
