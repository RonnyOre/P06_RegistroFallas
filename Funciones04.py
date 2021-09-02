import requests
import re
import sys
import time
from decimal import Decimal
from datetime import date, datetime, timedelta
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.request
from PyQt5 import *

url = 'https://www.multiplay.com.pe/consultas/consulta-prueba.php'


#-------------------------------- Funciones Generales ----------------------------------

def ejecutarSql(sql):
    datos = {'accion':'ejecutar','sql': sql}
    x = requests.post(url, data = datos)
    if x.text!="":
        respuesta=x.json()
        if respuesta!=[]:
            print(respuesta)
    else:
        print("respuesta vacía")
    return respuesta

def consultarSql(sql):
    datos = {'accion':'leer','sql': sql}
    x = requests.post(url, data=datos)
    respuesta=x.json()
    myresult=[]
    if respuesta!=[]:
        for datos in respuesta:
            contenido=[]
            for k,dato in datos.items():
                contenido.append(dato)
            myresult.append(contenido)
    return myresult

def cargarLogo(lb, codSoc):
    try:
        if codSoc == 'multiplay':
            codSoc = 'Mp_st'
        folderLogo = '''Logos/Logo'''+ codSoc +'.png'
        logoSoc = QPixmap(folderLogo)
        ratio = QtCore.Qt.KeepAspectRatio
        logoSoc = logoSoc.scaled(250, 35, ratio)
        lb.setPixmap(logoSoc)
    except:
        ""

def cargarIcono(obj, tipoIcono):
    try:
        iconos = {
        'erp': "organization",
        'banco':"banco",
        'grabar': "diskette",
        'modificar': "edit",
        'nuevo':"new_record",
        'direccion':"location",
        'salir': "logout",
        'buscar': "loupe",
        'compra':"purchasing",
        'usuario': "user",
        'darbaja': "x-button",
        'cargar': "sand-clock",
        'liberar': "liberar",
        'activar':"check",
        'cerrar':"close",
        'agregar_texto':'add_text',
        'consultar':"query",
        'con_texto':"with_text",
        'imprimir': "printer",
        'visualizar': "visualizar",
        'registrar': "clipboard",
        'condicion': "conditions",
        'depositar':"deposit",
        'importar':"data-transfer",
        'continuar':"right-arrow",
        'envio':"mail"}

        icono = iconos[tipoIcono]
        folderIcono = '''IconosLocales/'''+ icono +'.png'
        icon = QPixmap(folderIcono)
        if tipoIcono != 'erp':
            obj.setIcon(QIcon(icon))
        else:
            obj.setWindowIcon(QIcon(icon))
    except:
        ""

def mensajeDialogo(tipo, titulo, mensaje):
    try:
        msg = QMessageBox()
        cargarIcono(msg, 'erp')
        if tipo == 'error':
            msg.setIcon(QMessageBox.Critical)
        elif tipo == 'informacion':
            msg.setIcon(QMessageBox.Information)
        elif tipo == 'advertencia':
            msg.setIcon(QMessageBox.Warning)
        elif tipo == 'pregunta':
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setStyleSheet('''QMessageBox {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(160, 160, 160, 255), stop:1 rgba(255, 255, 255, 255));} ''')
        valor = msg.exec_()
        if valor == 1024:
            valor = 'Ok'
        if valor == 16384:
            valor = 'Yes'
        if valor == 65536:
            valor = 'No'
        return valor
    except:
        ""

def convlist(sql):
    informacion=consultarSql(sql)
    lista = []
    for info in informacion:
        for elemento in info:
            lista.append(elemento)
    return lista

def insertarDatos(cb, Datos):
    cb.clear()
    for dato in Datos:
        cb.addItem(dato[0])

def buscarTabla(tw, texto, columnas):
    try:
        rango = range(tw.topLevelItemCount())
        palabras=re.sub(' +', ' ', texto).split(" ")
        patrones=[]
        for palabra in palabras:
            patrones.append(re.compile(palabra.upper()))
        if texto=="":
            for i in rango:
                tw.topLevelItem(i).setHidden(False)
        else:
            for i in rango:
                busqueda=True
                for j in columnas:
                    subBusqueda=False
                    for patron in patrones:
                        subBusqueda=subBusqueda or (patron.search(tw.topLevelItem(i).text(j).upper()) is None)
                    busqueda=busqueda and subBusqueda
                if busqueda:
                    tw.topLevelItem(i).setHidden(True)
                else:
                    tw.topLevelItem(i).setHidden(False)
    except Exception as e:
        mensajeDialogo("error", "buscarTabla", e)

def formatearFecha(fecha):
    if fecha=="":
        return ""
    fecha=fecha.split("-")
    fecha.reverse()
    return "-".join(fecha)

def formatearDecimal(str, nro):
    try:
        decimal = float(str)
        decimalRound = round(decimal,int(nro))
        cantDecimales = "{:,." + nro + "f}"
        decimalStr = cantDecimales.format(decimalRound)
        return decimalStr
    except:
        ""

def QDateToStrView(Qdate):
    a1=str(Qdate.date().year())
    m1=str(Qdate.date().month())
    d1=str(Qdate.date().day())

    if len(d1)==1:
        d1='0'+d1
    if len(m1)==1:
        m1='0'+m1
    # strFecha="%s-%s-%s" % (a1,m1,d1)
    strFecha="%s-%s-%s" % (d1,m1,a1)
    return strFecha


#--------------------------------PROGRAMA N° 1 - ERP_DATA_REF_P002----------------------------------


#--------------------------------PROGRAMA N° 2 - ERP_ORG_P004----------------------------------

def actualizar(tw,sql):
    tw.clearContents()
    informacion=consultarSql(sql)
    flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    row=0
    for fila in informacion:
        col=0
        for i in fila:
            if i!=fila[3]:
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, col, item)
                col += 1
        if fila[3]=="1":
            C4=QTableWidgetItem(str("ACTIVO"))
            C4.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row, 4, C4)
        else:
            C4=QTableWidgetItem(str("BAJA"))
            C4.setFlags(flags)
            font = QtGui.QFont()
            font.setPointSize(12)
            C4.setFont(font)
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            C4.setForeground(brush)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row, 4, C4)
        row+=1

def NombreUbigeo(CodPais,CodDepartamento,CodProvincia,CodDistrito,TablaUbigeo):
    NombreUBI={}
    try:
        NombreUBI["Pais"]=TablaUbigeo[CodPais+"-0-0-0"]
    except:
        NombreUBI["Pais"]=""
    if NombreUBI["Pais"]=="Peru":
        try:
            if CodDepartamento!="0":
                NombreUBI["Departamento"]=TablaUbigeo[CodPais+"-"+CodDepartamento+"-0-0"]
            else:
                NombreUBI["Departamento"]=""
        except:
            NombreUBI["Departamento"]=""
        try:
            if CodProvincia!="0" and CodDepartamento!="0":
                NombreUBI["Provincia"]=TablaUbigeo[CodPais+"-"+CodDepartamento+"-"+CodProvincia+"-0"]
            else:
                NombreUBI["Provincia"]=""
        except:
            NombreUBI["Provincia"]=""
        try:
            if CodDistrito!="0" and CodProvincia!="0" and CodDepartamento!="0":
                NombreUBI["Distrito"]=TablaUbigeo[CodPais+"-"+CodDepartamento+"-"+CodProvincia+"-"+CodDistrito]
            else:
                NombreUBI["Distrito"]=""
        except:
            NombreUBI["Distrito"]=""
    else:
        try:
            if CodDepartamento!="0":
                NombreUBI["Departamento"]=TablaUbigeo[CodPais+"-"+CodDepartamento+"-0-0"]
            else:
                NombreUBI["Departamento"]=""
        except:
            NombreUBI["Departamento"]=""
        NombreUBI["Provincia"]=""
        NombreUBI["Distrito"]=""
    return NombreUBI

def TablaUbigeo(sql):
    ubicacion=consultarSql(sql)
    tablaUbigeo={}
    for item in ubicacion:
        tablaUbigeo[item[0]+"-"+item[1]+"-"+item[2]+"-"+item[3]]=item[4]
    return tablaUbigeo


#--------------------------------PROGRAMA N° 3 - ERP_PROV_P001----------------------------------

def actualizarInter(self,tw,sql,Tipo_Inter,dicTipoInter):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb = QComboBox(tw)
            tw.setCellWidget(row, 0, cb)
            insertarDatos(cb,Tipo_Inter)
            cb.setEditable(True)
            for k,v in dicTipoInter.items():
                if fila[0]==k:
                    tw.cellWidget(row, 0).setEditText(v)
            font = QtGui.QFont()
            font.setPointSize(12)
            cb.setFont(font)
            # font = QFont('Times', 12)
            le = cb.lineEdit()
            le.setFont(font)
            tw.resizeColumnToContents(0)
            tw.cellWidget(row, 0).setEnabled(False)
            tw.cellWidget(row, 0).setStyleSheet("color: rgb(0,0,0);")

            col=1
            for i in fila:
                if i!=fila[0] and i!=fila[7]:
                    item=QTableWidgetItem(i)
                    item.setFlags(flags)
                    if tw.rowCount()<=row:
                        tw.insertRow(tw.rowCount())
                    tw.setItem(row, col, item)
                    col += 1

            if fila[7]=="1":
                C7=QTableWidgetItem(str("ACTIVO"))
                C7.setFlags(flags)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, 7, C7)
            else:
                C7=QTableWidgetItem(str("BAJA"))
                C7.setFlags(flags)
                font = QtGui.QFont()
                font.setPointSize(12)
                C7.setFont(font)
                brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                C7.setForeground(brush)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, 7, C7)
            row+=1
        rowPosi=tw.rowCount()
        tw.insertRow(rowPosi)
        item=QTableWidgetItem()
        item.setFlags(flags)
        tw.setItem(rowPosi,7, item)

        cb0 = QComboBox(tw)
        tw.setCellWidget(rowPosi, 0, cb0)
        insertarDatos(cb0,Tipo_Inter)
        cb0.setCurrentIndex(-1)
        font = QtGui.QFont()
        font.setPointSize(12)
        cb0.setFont(font)
        tw.resizeColumnToContents(0)

    else:
        cb = QComboBox(tw)
        tw.setCellWidget(0, 0, cb)
        insertarDatos(cb,Tipo_Inter)
        cb.setCurrentIndex(-1)
        font = QtGui.QFont()
        font.setPointSize(12)
        cb.setFont(font)
        tw.resizeColumnToContents(0)

        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item=QTableWidgetItem()
        item.setFlags(flags)
        tw.setItem(0,7, item)

def actualizarBan(self,tw,sql,datos,TCta,dicbanco,banco,dicmoneda,mon):
    tw.clearContents()

    informacion=consultarSql(sql)

    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            C0=QTableWidgetItem(fila[0])
            C0.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,0, C0)
            tw.resizeColumnToContents(0)

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb1 = QComboBox(tw)
            # cb1.setEditable(True)
            tw.setCellWidget(row, 1, cb1)
            llenarPais(datos,cb1)
            cb1.setCurrentIndex(int(fila[1])-1)
            # tw.cellWidget(row, 1).setEditText(fila[1])
            font = QtGui.QFont()
            font.setPointSize(12)
            cb1.setFont(font)
            tw.resizeColumnToContents(1)
            tw.cellWidget(row, 1).setEnabled(False)
            tw.cellWidget(row, 1).setStyleSheet("color: rgb(0,0,0);")
            cb1.activated.connect(self.cargarDepartamento)

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb2 = QComboBox(tw)
            # cb2.setEditable(True)
            tw.setCellWidget(row, 2, cb2)
            Paisx=fila[1]
            llenarDepartamento(datos,cb2,Paisx)
            cb2.setCurrentText(fila[2])
            # tw.cellWidget(row, 2).setEditText(fila[2])
            font = QtGui.QFont()
            font.setPointSize(12)
            cb2.setFont(font)
            tw.resizeColumnToContents(2)
            tw.cellWidget(row, 2).setEnabled(False)
            tw.cellWidget(row, 2).setStyleSheet("color: rgb(0,0,0);")

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb3 = QComboBox(tw)
            # cb3.setEditable(True)
            tw.setCellWidget(row, 3, cb3)
            insertarDatos(cb3,banco)
            cb3.setCurrentIndex(int(fila[3])-1)
            # tw.cellWidget(row, 3).setEditText(fila[3])
            font = QtGui.QFont()
            font.setPointSize(12)
            cb3.setFont(font)
            tw.resizeColumnToContents(3)
            tw.cellWidget(row, 3).setEnabled(False)
            tw.cellWidget(row, 3).setStyleSheet("color: rgb(0,0,0);")

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb4 = QComboBox(tw)
            # cb4.setEditable(True)
            tw.setCellWidget(row, 4, cb4)
            for k,v in TCta.items():
                cb4.addItem(k)
            if fila[4]=="CA":
                cb4.setCurrentIndex(0)
            elif fila[4]=="CC":
                cb4.setCurrentIndex(1)
            font = QtGui.QFont()
            font.setPointSize(12)
            cb4.setFont(font)
            tw.resizeColumnToContents(4)
            tw.cellWidget(row,4).setEnabled(False)
            tw.cellWidget(row,4).setStyleSheet("color: rgb(0,0,0);")

            C5=QTableWidgetItem(fila[5])
            C5.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,5, C5)

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb6 = QComboBox(tw)
            # cb6.setEditable(True)
            tw.setCellWidget(row, 6, cb6)
            insertarDatos(cb6,mon)

            cb6.setCurrentIndex(int(fila[6])-1)
            # tw.cellWidget(row, 8).setEditText(fila[6])
            font = QtGui.QFont()
            font.setPointSize(12)
            cb6.setFont(font)
            tw.resizeColumnToContents(6)
            tw.cellWidget(row, 6).setEnabled(False)
            tw.cellWidget(row, 6).setStyleSheet("color: rgb(0,0,0);")

            C7=QTableWidgetItem(fila[7])
            C7.setFlags(flags)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setItem(row,7, C7)

            if fila[8]=="1":
                C8=QTableWidgetItem(str("ACTIVO"))
                C8.setFlags(flags)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row,8, C8)
            else:
                C8=QTableWidgetItem(str("BAJA"))
                C8.setFlags(flags)
                font = QtGui.QFont()
                font.setPointSize(12)
                C8.setFont(font)
                brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                C8.setForeground(brush)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, 8, C8)
            row+=1

        rowPosi=tw.rowCount()
        tw.insertRow(rowPosi)

        CB0 = QComboBox(tw)
        tw.setCellWidget(rowPosi, 1, CB0)
        for k,v in datos.items():
            codigo=k.split("-")
            if "-".join(codigo[1:])=="0-0-0":
                CB0.addItem(v)
        CB0.setCurrentIndex(-1)
        # CB0.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        CB0.setFont(font)
        tw.resizeColumnToContents(1)
        CB0.activated.connect(self.cargarDepartamento)

        #creacion combo departamento...
        CB1 = QComboBox(tw)
        tw.setCellWidget(rowPosi, 2, CB1)
        CB1.setCurrentIndex(-1)
        # CB1.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        CB1.setFont(font)
        tw.resizeColumnToContents(2)

        #creacion combo tipo de banco...
        CB2 = QComboBox(tw)
        tw.setCellWidget(rowPosi, 3, CB2)
        insertarDatos(CB2,banco)
        CB2.setCurrentIndex(-1)
        # CB2.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        CB2.setFont(font)
        tw.resizeColumnToContents(3)

        #creacion combo tipo de cuenta...
        CB3 = QComboBox(tw)
        tw.setCellWidget(rowPosi, 4, CB3)
        for k,v in TCta.items():
            CB3.addItem(k)
        CB3.setCurrentIndex(-1)
        # CB3.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        CB3.setFont(font)
        tw.resizeColumnToContents(4)

        CB4 = QComboBox(tw)
        tw.setCellWidget(rowPosi, 6, CB4)
        insertarDatos(CB4,mon)
        CB4.setCurrentIndex(-1)
        # CB4.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        CB4.setFont(font)
        tw.resizeColumnToContents(6)

        Nro=QTableWidgetItem(str(rowPosi+1))
        Nro.setFlags(flags)
        tw.setItem(rowPosi,0, Nro)

        item=QTableWidgetItem()
        item.setFlags(flags)
        tw.setItem(rowPosi,8, item)
        tw.resizeColumnToContents(0)

    else:
        cb0 = QComboBox(tw)
        tw.setCellWidget(0, 1, cb0)
        for k,v in datos.items():
            codigo=k.split("-")
            if "-".join(codigo[1:])=="0-0-0":
                cb0.addItem(v)
        cb0.setCurrentIndex(-1)
        # cb0.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb0.setFont(font)
        tw.resizeColumnToContents(1)
        cb0.activated.connect(self.cargarDepartamento)

        #creacion combo departamento...
        cb1 = QComboBox(tw)
        tw.setCellWidget(0, 2, cb1)
        cb1.setCurrentIndex(-1)
        # cb1.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb1.setFont(font)
        tw.resizeColumnToContents(2)

        #creacion combo tipo de banco...
        cb2 = QComboBox(tw)
        tw.setCellWidget(0, 3, cb2)
        insertarDatos(cb2,banco)
        cb2.setCurrentIndex(-1)
        # cb2.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb2.setFont(font)
        tw.resizeColumnToContents(3)

        #creacion combo tipo de cuenta...
        cb3 = QComboBox(tw)
        tw.setCellWidget(0, 4, cb3)
        for k,v in TCta.items():
            cb3.addItem(k)
        cb3.setCurrentIndex(-1)
        # cb3.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb3.setFont(font)
        tw.resizeColumnToContents(4)

        cb4 = QComboBox(tw)
        tw.setCellWidget(0, 6, cb4)
        insertarDatos(cb4,mon)
        cb4.setCurrentIndex(-1)
        # cb4.setStyleSheet("background-color: rgb(255,255,255);")
        font = QtGui.QFont()
        font.setPointSize(12)
        cb4.setFont(font)
        tw.resizeColumnToContents(6)

        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        Nro=QTableWidgetItem("1")
        Nro.setFlags(flags)
        tw.setItem(0,0, Nro)

        item=QTableWidgetItem()
        item.setFlags(flags)
        tw.setItem(0,8, item)
        tw.resizeColumnToContents(0)

def actualizarComp(tw,sql):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            tw.resizeColumnToContents(0)
            tw.resizeColumnToContents(5)
            col=0
            for i in fila:
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                # item.setTextAlignment(QtCore.Qt.AlignHCenter)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, col, item)
                # tw.resizeColumnToContents(col)
                col += 1
            row+=1
        rowPosi=tw.rowCount()
        tw.insertRow(rowPosi)
        Nro=QTableWidgetItem(str(rowPosi+1))
        Nro.setFlags(flags)
        tw.setItem(rowPosi,0, Nro)
        tw.resizeColumnToContents(0)
        tw.resizeColumnToContents(5)
    else:
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        Nro=QTableWidgetItem("1")
        Nro.setFlags(flags)
        tw.setItem(0,0, Nro)
        tw.resizeColumnToContents(0)
        tw.resizeColumnToContents(5)

def llenarPais(TablaUbigeo,cbPais):  #Codigo pais va 0
    for ubigeo,nombre in TablaUbigeo.items():
        au=ubigeo.find("-")
        bu=ubigeo.find("-",au+1)
        cu=ubigeo.find("-",bu+1)
        if ubigeo[au+1:]=="0-0-0":
            cbPais.addItem(nombre)

def llenarDepartamento(TablaUbigeo,cbDepartamento,codigoPais):  #Codigo pais va 0
    for ubigeo,nombre in TablaUbigeo.items():
        au=ubigeo.find("-")
        bu=ubigeo.find("-",au+1)
        cu=ubigeo.find("-",bu+1)
        if ubigeo[:au]==codigoPais and ubigeo[au+1:]!="0-0-0" and ubigeo[bu+1:]=="0-0":
            cbDepartamento.addItem(nombre)

def llenarDep(TablaUbigeo,cbDepartamento,codigoPais):  #Codigo pais va 0
    cbDepartamento.clear()
    for ubigeo,nombre in TablaUbigeo.items():
        au=ubigeo.find("-")
        bu=ubigeo.find("-",au+1)
        cu=ubigeo.find("-",bu+1)
        if ubigeo[:au]==codigoPais and ubigeo[au+1:]!="0-0-0" and ubigeo[bu+1:]=="0-0":
            cbDepartamento.addItem(ubigeo[au+1:bu]+" - "+nombre)
            cbDepartamento.setCurrentIndex(-1)

def verificarTIP(tw):
    TIP=[]
    A=tw.rowCount()
    B=tw.currentRow()
    for fila in range(A-(A-B)):
        item=tw.cellWidget(fila, 0).currentText()
        TIP.append(item)
    return TIP

###############################################################

def consultaRuc(mostrar, RUC):
    try:
        print("Primer método")
        respuesta=consultaRucPeruApis(mostrar, RUC) #Razon Social y Nombre Comercial
        if respuesta!=False:
            return respuesta
    except Exception as e:
        mensajeDialogo("error", "Primer método", "%s\nRUC:%s" % (e, RUC))

    try:
        print("Segundo método")
        respuesta=consultaRucApiSPeru(mostrar, RUC) #Menos Nombre Comercial
        if respuesta!=False:
            return respuesta
    except Exception as e:
        mensajeDialogo("error", "Segundo método", "%s\nRUC:%s" % (e, RUC))

    try:
        print("Tercer método")
        respuesta=consultaRucApiPeruDev(mostrar, RUC) #Direccion completa falta Distrito Departamento Provincia
        if respuesta!=False:
            return respuesta
    except Exception as e:
        mensajeDialogo("error", "Tercer método", "%s\nRUC:%s" % (e, RUC))

    try:
        print("Cuarto método")
        respuesta=consultaRucMigo(mostrar, RUC)
        if respuesta!=False:
            return respuesta
    except Exception as e:
        mensajeDialogo("error", "Cuarto método", "%s\nRUC:%s" % (e, RUC))

def consultaRucPeruApis(mostrar, RUC): #Razon Social y Nombre Comercial Check
    continuar=True
    if len(RUC)<8: return False
    try:
        tokenRUC="QLDGyWjlG4EZU11WJ0gcVO7wcBC5mzPR8CWEBx09N0qXNk7GvPerz6Y8WPXK" #Token Personal
        headers = {"Authorization" : "Bearer %s" % tokenRUC, 'Content-Type':'application/json'}

        if len(RUC)==8:
            url="https://api.peruapis.com/v1/dni"
            r = requests.post(url, data=json.dumps({"document":"%s" % RUC}), headers=headers)
            print(r.text)
            if not r.ok:
                if mostrar:
                    mensajeDialogo("informacion", "Consulta RUC", "No se encontró el RUC " + str(RUC))
                return False
            data=r.json()
            Ruc=data["data"]["dni"]
            RazonSocial=data["data"]["fullname"]
            Codigo=data["data"]["verification_code"]
            NombreComercial="-"
            Direccion=""
            Ubigeo=""
            Descripcion=""
            Estado=""

            url="https://api.peruapis.com/v1/ruc"
            r = requests.post(url, data=json.dumps({"document":"10%s%s" % (RUC, Codigo)}), headers=headers)
            print(r.text)

            if not r.ok:
                continuar=False

            if continuar:
                data=r.json()
                Ruc=data["data"]["ruc"]
                RazonSocial=data["data"]["name"]
                NombreComercial=data["data"]["commercial_name"]
                if NombreComercial==None:
                    NombreComercial="-"
                Distrito=data["data"]["district"]
                Provincia=data["data"]["province"]
                Departamento=data["data"]["region"]
                if Distrito==None:
                    Descripcion=""
                    Direccion="-"
                else:
                    Descripcion="%s-%s-%s" % (Distrito, Provincia, Departamento)
                    Direccion=data["data"]["address"] + " " + Descripcion
                Ubigeo=data["data"]["location"]
                Estado=data["data"]["status"]
        else:
            url="https://api.peruapis.com/v1/ruc"
            r = requests.post(url, data=json.dumps({"document":"%s" % RUC}), headers=headers)
            print(r.text)
            if not r.ok:
                if mostrar:
                    mensajeDialogo("informacion", "Consulta RUC", "No se encontró el RUC " + str(RUC))
                return False
            data=r.json()
            Ruc=data["data"]["ruc"]
            RazonSocial=data["data"]["name"]
            NombreComercial=data["data"]["commercial_name"]
            if NombreComercial==None:
                NombreComercial="-"
            Distrito=data["data"]["district"]
            Provincia=data["data"]["province"]
            Departamento=data["data"]["region"]
            if Distrito==None:
                Descripcion=""
                Direccion="-"
            else:
                Descripcion="%s-%s-%s" % (Distrito, Provincia, Departamento)
                Direccion=data["data"]["address"] + " " + Descripcion
            Ubigeo=data["data"]["location"]
            Estado=data["data"]["status"]
    except Exception as e:
        if mostrar:
            mensajeDialogo("error", "consultaRucPeruApis", "%s\nRUC:%s" % (e, RUC))
        return False
    return [Ruc, RazonSocial, NombreComercial, Direccion, Estado, Ubigeo, Descripcion]

def consultaRucApiSPeru(mostrar, RUC): #Nombre Comercial Check
    continuar=True
    if len(RUC)<8: return False
    try:
        token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJvbm55Lm9hLjE0QGdtYWlsLmNvbSJ9.8rOVuY6r1UK1GJlimZjxSH3u8ONw83kQoBV85V6mQeE" # Token Personal
        if len(RUC)==8:
            tipo="dni"
        else:
            tipo="ruc"
        url="https://dniruc.apisperu.com/api/v1/%s/%s?token=%s" % (tipo, RUC, token)
        r = requests.get(url)
        print(r.text)
        if not r.ok:
            if "504 Gateway Time-out" in r.text:
                print("Error en la página")
                a=float("hola")
            if "Ha excedido" in r.text:
                print("Exceso de consultas")
                a=float("hola")
            mensajeDialogo("informacion", "Consulta RUC", "No se encontró el RUC " + str(RUC))
            return False
        data=r.json()
        if tipo=="ruc":
            Ruc=data["ruc"]
            RazonSocial=data["razonSocial"]
            NombreComercial=data["nombreComercial"]
            if data["direccion"]!="-":
                Departamento=data["departamento"]
                Provincia=data["provincia"]
                Distrito=data["distrito"]
                Direccion="%s %s - %s - %s" % (data["direccion"], Departamento, Provincia, Distrito)
                respuesta=consultarSql(sqlUbigeoRuc % (Departamento, Provincia, Distrito))
                if respuesta==[]:
                    Ubigeo=""
                    Descripcion=""
                else:
                    Ubigeo=respuesta[0][0]
                    Descripcion=respuesta[0][1]
            else:
                Direccion="-"
                Ubigeo=""
                Descripcion=""
            Estado=data["estado"]
        else:
            ruc="10" + data["dni"] + data["codVerifica"]
            url="https://dniruc.apisperu.com/api/v1/ruc/%s?token=%s" % (ruc, token)
            r = requests.get(url)
            if not r.ok:
                Ruc=data["dni"]
                RazonSocial="%s %s %s" % (data["apellidoPaterno"], data["apellidoMaterno"], data["nombres"])
                NombreComercial="-"
                Direccion="-"
                Ubigeo=""
                Descripcion=""
                Estado="SIN RUC"
            else:
                data=r.json()
                Ruc=data["ruc"]
                RazonSocial=data["razonSocial"]
                NombreComercial=data["nombreComercial"]
                Direccion="-"
                Ubigeo=""
                Descripcion=""
                Estado=data["estado"]
    except Exception as e:
        if mostrar:
            mensajeDialogo("error", "consultaRucApiSPeru", "%s\nRUC:%s" % (e, RUC))
        return False
    return [Ruc, RazonSocial, NombreComercial, Direccion, Estado, Ubigeo, Descripcion]

def consultaRucApiPeruDev(mostrar, RUC): #Direccion completa Check
    continuar=True
    if len(RUC)<8: return False
    try:
        tokenRUC="dea2d1928a82aaaac3dd17c37d9647f2de56cc835d77fb11d3404a9133efa0c3" #Token Personal
        headers = {"Authorization" : "Bearer %s" % tokenRUC, 'Content-Type': 'application/json'}

        if len(RUC)==8:
            url="https://apiperu.dev/api/dni/%s" % RUC
            r = requests.get(url, headers=headers)
            print(r.text)
            if not r.ok:
                mensajeDialogo("informacion", "Consulta RUC", "No se encontró el RUC " + str(RUC))
                return False
            data=r.json()
            Ruc=data["data"]["ruc"]
            RazonSocial=data["data"]["nombre_completo"]
            Codigo=data["data"]["codigo_verificacion"]
            NombreComercial=""
            Direccion=""
            Ubigeo=""
            Descripcion=""
            Estado=""

            url="https://apiperu.dev/api/ruc/10%s%s" % (RUC, Codigo)
            r = requests.get(url, headers=headers)
            print(r.text)
            if not r.ok:
                continuar=False
            if continuar:
                data=r.json()
                Ruc=data["data"]["ruc"]
                RazonSocial=data["data"]["nombre_o_razon_social"]
                NombreComercial=""
                if "direccion_completa" in data["data"]:
                    Direccion=data["data"]["direccion_completa"]
                else:
                    Direccion=""
                Ubigeo=data["data"]["ubigeo"][2]
                Descripcion=""
                Estado=data["data"]["estado"]
        else:
            url="https://apiperu.dev/api/ruc/%s" % RUC
            r = requests.get(url, headers=headers)
            print(r.text)
            if not r.ok:
                mensajeDialogo("informacion", "Consulta RUC", "No se encontró el RUC " + str(RUC))
                return False
            data=r.json()
            Ruc=data["data"]["ruc"]
            RazonSocial=data["data"]["nombre_o_razon_social"]
            NombreComercial=""
            if "direccion_completa" in data["data"]:
                Direccion=data["data"]["direccion_completa"]
            else:
                Direccion=""
            Ubigeo=data["data"]["ubigeo"][2]
            Descripcion=""
            Estado=data["data"]["estado"]

    except Exception as e:
        if mostrar:
            mensajeDialogo("error", "consultaRucApiPeruDev", "%s\nRUC:%s" % (e, RUC))
        return False
    return [Ruc, RazonSocial, NombreComercial, Direccion, Estado, Ubigeo, Descripcion]

def consultaRucMigo(mostrar, RUC):
    if len(RUC)<8: return False
    try:
        tokenRUC="jRdhFs3PVRqow7h9Aiev7JjkX2gtELMFXb7yfhbBaCVmqGgtPlSGYWTxt6wG" #Api Migo token Personal 2021/07/14
        headers = {'Content-Type':'application/json'}

        if len(RUC)==8:
            url="https://api.migo.pe/api/v1/dni"
            data = '{"token":"%s", "dni":"%s"}' % (tokenRUC, RUC)
            print(data, url)
            r = requests.post(url, data=data, headers=headers)
            print(r.text)
            if not r.ok:
                if mostrar:
                    mensajeDialogo("informacion", "Consulta RUC", "No se encontró el RUC " + str(RUC))
                return False
            data=r.json()
            if data["success"]:
                Ruc=data["dni"]
                RazonSocial=data["nombre"]
                Codigo="-"
                NombreComercial="-"
                Direccion="-"
                Ubigeo=""
                Descripcion=""
                Estado=""
            else:
                if mostrar:
                    mensajeDialogo("informacion", "Consulta RUC", "No se encontró el RUC " + str(RUC))
                return False
        else:
            url="https://api.migo.pe/api/v1/ruc"
            data = '{"token":"%s", "ruc":"%s"}' % (tokenRUC, RUC)
            print(data, url)
            r = requests.post(url, data=data, headers=headers)
            print(r.text)
            if not r.ok:
                if mostrar:
                    mensajeDialogo("informacion", "Consulta RUC", "No se encontró el RUC " + str(RUC))
                return False
            data=r.json()
            if data["success"]:
                Ruc=data["ruc"]
                RazonSocial=data["nombre_o_razon_social"]
                NombreComercial="-"
                Distrito=data["distrito"]
                Provincia=data["provincia"]
                Departamento=data["departamento"]
                if Distrito==None:
                    Descripcion=""
                    Direccion="-"
                else:
                    Descripcion="%s-%s-%s" % (Distrito, Provincia, Departamento)
                    Direccion=data["direccion_simple"] + " " + Descripcion
                Ubigeo=data["ubigeo"]
                Estado=data["estado_del_contribuyente"]
            else:
                if mostrar:
                    mensajeDialogo("informacion", "Consulta RUC", "No se encontró el RUC " + str(RUC))
                return False

    except Exception as e:
        if mostrar:
            mensajeDialogo("error", "consultaRucMigo", "%s\nRUC:%s" % (e, RUC))
        return False
    return [Ruc, RazonSocial, NombreComercial, Direccion, Estado, Ubigeo, Descripcion]

#################################################################################################################

#--------------------------------PROGRAMA N° 4 - ERP_REQ_P002----------------------------------

def Cargar(self,tw,sql,Inicio,Final,Fec_Inicial,Fec_Final,Cod_Soc,Año):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            fila[1]=formatearFecha(fila[1])
            fila[2]=formatearFecha(fila[2])
            sqlMonto="SELECT SUM(Cant_Mat_Serv*Precio_ref) FROM TAB_SOLP_002_Detalle_Solicitud_Pedido WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Solp='%s'"%(Cod_Soc,Año,fila[0])
            Monto=convlist(sqlMonto)
            mont=formatearDecimal(Monto[0],'3')
            fila.insert(6,mont)
            col=0
            for i in fila:
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row,col, item)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                tw.resizeColumnToContents(3)
                tw.resizeColumnToContents(4)
                col += 1

            pb = QPushButton("Consultar",tw)
            tw.setCellWidget(row, 6, pb)
            cargarIcono(pb,'consultar')
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            pb.setFont(font)
            pb.setStyleSheet("background-color: rgb(255, 213, 79);")
            pb.clicked.connect(self.Consultar)
            tw.resizeColumnToContents(6)

            row+=1
    else:
        mensajeDialogo("error", "Error","No se encontraron solicitudes de pedido en este rango")
        Inicio.setCurrentIndex(-1)
        Final.setCurrentIndex(-1)
        Fec_Inicial.clear()
        Fec_Final.clear()

def actualizarSOLP(self,tw,sql,Estado_Doc,Cod_Soc,NroSOLP,Año):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            fila[6]=formatearDecimal(fila[6],'3')
            fila[7]=formatearDecimal(fila[7],'2')
            fila[8]=formatearFecha(fila[8])
            for k,v in Estado_Doc.items():
                if fila[0]==k:
                    C0=QTableWidgetItem(v)
                    C0.setFlags(flags)
                    C0.setTextAlignment(QtCore.Qt.AlignCenter)
                    if v=='Anulado':
                        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                        brush.setStyle(QtCore.Qt.SolidPattern)
                        C0.setForeground(brush)
                    elif v=='Aprobado':
                        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
                        brush.setStyle(QtCore.Qt.SolidPattern)
                        C0.setForeground(brush)
                    if tw.rowCount()<=row:
                        tw.insertRow(tw.rowCount())
                    tw.setItem(row, 0, C0)
                    tw.resizeColumnToContents(0)

            C1=QTableWidgetItem(fila[1])
            C1.setFlags(flags)
            C1.setTextAlignment(QtCore.Qt.AlignCenter)
            brush = QtGui.QBrush(QtGui.QColor(85, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            C1.setBackground(brush)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.resizeColumnToContents(1)
            tw.setItem(row, 1, C1)

            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb0=QComboBox(tw)
            tw.setCellWidget(row,2,cb0)
            tw.cellWidget(row,2).addItem(fila[2])
            font = QtGui.QFont()
            font.setPointSize(12)
            cb0.setFont(font)
            tw.resizeColumnToContents(2)
            tw.cellWidget(row,2).setEnabled(False)

            material=[fila[3],fila[4],fila[5],fila[6],fila[7],fila[8],fila[9]]
            col=3
            for i in material:
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, col, item)
                tw.resizeColumnToContents(col)
                col+=1

            combo=[fila[10],fila[11],fila[12],fila[13]]
            c=10
            for i in combo:
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                cb1=QComboBox(tw)
                tw.setCellWidget(row,c,cb1)
                tw.cellWidget(row,c).addItem(i)
                font = QtGui.QFont()
                font.setPointSize(12)
                cb1.setFont(font)
                tw.resizeColumnToContents(c)
                tw.cellWidget(row,c).setEnabled(False)
                c+=1

            sqlTexto="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s'AND Año='%s' AND Tipo_Proceso='1'AND Nro_Doc='%s'AND Item_Doc='%s'"%(Cod_Soc,Año,NroSOLP,fila[1])
            texto=consultarSql(sqlTexto)

            btTexto=QPushButton(tw)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setCellWidget(row, 14, btTexto)

            if texto!=[]:
                cargarIcono(btTexto,'con_texto')
            elif texto==[]:
                cargarIcono(btTexto,'agregar_texto')

            tw.resizeColumnToContents(14)
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            btTexto.setFont(font)
            btTexto.setStyleSheet("background-color: rgb(255, 213, 79);")
            btTexto.clicked.connect(self.TextoPosicion)
            row+=1

def actualizarboton(self,tw,Cod_Soc,Año,Numero_Solp,Item_Solp,row):
    sqlTexto="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s'AND Año='%s' AND Tipo_Proceso='1'AND Nro_Doc='%s'AND Item_Doc='%s'"%(Cod_Soc,Año,Numero_Solp,Item_Solp)
    texto=consultarSql(sqlTexto)

    btTexto=QPushButton(tw)
    tw.setCellWidget(row, 14, btTexto)

    if texto!=[]:
        cargarIcono(btTexto,'con_texto')
    elif texto==[]:
        cargarIcono(btTexto,'agregar_texto')

    tw.resizeColumnToContents(14)
    font = QtGui.QFont()
    font.setPointSize(11)
    font.setBold(True)
    btTexto.setFont(font)
    btTexto.setStyleSheet("background-color: rgb(255, 213, 79);")
    btTexto.clicked.connect(self.TextoPosicion)

#--------------------------------PROGRAMA N° 5 - ERP_COMP_P001----------------------------------

def CargarCotApro(self,tw,sql,Cod_Soc,dicProv,Año):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            fila[3]=formatearFecha(fila[3])
            fila[5]=formatearFecha(fila[5])
            try:
                for k,v in dicProv.items():
                    if fila[1]==v:
                        Cod_Prov=k
                sqlCabPed="SELECT Estado_Pedido FROM TAB_COMP_004_Pedido_Compra WHERE Cod_Emp='%s'AND Cod_Prov='%s' AND Nro_Cotiza='%s'"%(Cod_Soc,Cod_Prov,fila[0])
                CabPed=convlist(sqlCabPed)

                if CabPed!=[]:
                    fila.insert(7,"EMITIDO")
            except:
                ""
            col=0
            for i in fila:
                if col==3:
                    for k,v in dicProv.items():
                        if fila[1]==v:
                            Cod_Prov=k
                    sqlMonto="SELECT SUM(Cant_Asignada*Precio_Cotiza) FROM TAB_COMP_002_Detalle_Cotización_de_Compra WHERE Cod_Soc='%s' AND Año='%s' AND Nro_Cotiza='%s' AND Cod_Prov='%s'"%(Cod_Soc,Año,fila[0],Cod_Prov)
                    Monto=convlist(sqlMonto)
                    mont=formatearDecimal(Monto[0],'3')
                    C3=QTableWidgetItem(mont)
                    C3.setFlags(flags)
                    C3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                    if tw.rowCount()<=row:
                        tw.insertRow(tw.rowCount())
                    tw.setItem(row,col, C3)
                    col+=1
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, col, item)
                tw.resizeColumnToContents(col)
                col += 1
            row+=1
    else:
        QMessageBox.critical(self, "Informacion","No se encontraron cotizaciones aprobadas en este rango, verifique", QMessageBox.Ok)

def CargarPedComp(self,tw,sql,Cod_Soc,Año,Nro_Doc):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item_ped=1
        row=0
        for fila in informacion:
            fila.insert(0,str(item_ped))
            fila[6]=formatearDecimal(fila[6],'3')
            fila[5]=formatearDecimal(fila[5],'3')
            col=0
            for i in fila:
                item=QTableWidgetItem(i)
                item.setFlags(flags)
                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, col, item)
                tw.resizeColumnToContents(col)

                col += 1

            sqlTexto="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s'AND Año='%s' AND Tipo_Proceso='3'AND Nro_Doc='%s'AND Item_Doc='%s'"%(Cod_Soc,Año,Nro_Doc,fila[0])
            texto=consultarSql(sqlTexto)

            btTexto=QPushButton(tw)
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            tw.setCellWidget(row, 11, btTexto)

            if texto!=[]:
                cargarIcono(btTexto,'con_texto')
            elif texto==[]:
                cargarIcono(btTexto,'agregar_texto')

            # tw.resizeColumnToContents(11)
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            btTexto.setFont(font)
            btTexto.setStyleSheet("background-color: rgb(255, 213, 79);")
            btTexto.clicked.connect(self.TextoPosicion)
            row+=1
            item_ped=int(item_ped)+1
    # else:
    #     QMessageBox.critical(self, "Informacion","No se encontraron datos", QMessageBox.Ok)

def actualizarboton2(self,tw,Cod_Soc,Año,Nro_Doc,Item_Solp,row):
    sqlTexto="SELECT Texto FROM TAB_SOC_019_Texto_Proceso WHERE Cod_Soc='%s'AND Año='%s' AND Tipo_Proceso='3'AND Nro_Doc='%s'AND Item_Doc='%s'"%(Cod_Soc,Año,Nro_Doc,Item_Solp)
    texto=consultarSql(sqlTexto)

    btTexto=QPushButton(tw)
    tw.setCellWidget(row, 11, btTexto)

    if texto!=[]:
        cargarIcono(btTexto,'con_texto')
    elif texto==[]:
        cargarIcono(btTexto,'agregar_texto')

    # tw.resizeColumnToContents(11)
    font = QtGui.QFont()
    font.setPointSize(11)
    font.setBold(True)
    btTexto.setFont(font)
    btTexto.setStyleSheet("background-color: rgb(255, 213, 79);")
    btTexto.clicked.connect(self.TextoPosicion)

def cargarInter(tw,sql,Tipo_Inter,dicTipoInter):
    tw.clearContents()
    informacion=consultarSql(sql)
    if informacion!=[]:
        rows=tw.rowCount()
        for r in range(rows):
            tw.removeRow(1)
        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        row=0
        for fila in informacion:
            if tw.rowCount()<=row:
                tw.insertRow(tw.rowCount())
            cb = QComboBox(tw)
            tw.setCellWidget(row, 0, cb)
            for k,v in dicTipoInter.items():
                if fila[0]==k:
                    tw.cellWidget(row, 0).addItem(v)
            font = QtGui.QFont()
            font.setPointSize(12)
            cb.setFont(font)
            tw.resizeColumnToContents(0)
            tw.cellWidget(row, 0).setEnabled(False)

            col=1
            for i in fila:
                if i!=fila[0] and i!=fila[7]:
                    item=QTableWidgetItem(i)
                    item.setFlags(flags)
                    item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                    if tw.rowCount()<=row:
                        tw.insertRow(tw.rowCount())
                    tw.setItem(row, col, item)
                    col += 1

            if fila[7]=="1":
                C7=QTableWidgetItem(str("ACTIVO"))
                C7.setFlags(flags)
                C7.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                if tw.rowCount()<=row:
                    tw.insertRow(tw.rowCount())
                tw.setItem(row, 7, C7)
            row+=1
    else:
        cb = QComboBox(tw)
        tw.setCellWidget(0, 0, cb)
        insertarDatos(cb,Tipo_Inter)
        cb.setCurrentIndex(-1)
        font = QtGui.QFont()
        font.setPointSize(12)
        cb.setFont(font)
        tw.resizeColumnToContents(0)

        flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        item=QTableWidgetItem()
        item.setFlags(flags)
        tw.setItem(0,7, item)

def condPos(self,tw,sql,Cond_Comp,Cond_Comp1,Cond_Comp2,Cond_Comp3,dicCond_Comp,Precio,Valor,Moneda,Tipo_Pedido):
    informacion=consultarSql(sql)
    flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    if informacion!=[]:
        row=0
        for fila in informacion:
            for k,v in dicCond_Comp.items():
                if fila[0]==v:
                    condcomp=k
            if int(condcomp)<6:
                if tw.rowCount()-3<=row:
                    tw.insertRow(tw.rowCount()-3)
                cb = QComboBox(tw)
                tw.setCellWidget(row, 0, cb)
                insertarDatos(cb,Cond_Comp)
                tw.cellWidget(row, 0).setCurrentText(fila[0])
                font = QtGui.QFont()
                font.setPointSize(12)
                cb.setFont(font)
                tw.resizeColumnToContents(0)
                tw.cellWidget(row, 0).setEnabled(False)

                col=1
                for i in fila:
                    if i=='0.00':
                        i=""
                    if i!=fila[0]:
                        celda=QTableWidgetItem(i)
                        celda.setFlags(flags)
                        celda.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                        if tw.rowCount()-3<=row:
                            tw.insertRow(tw.rowCount()-3)
                        tw.setItem(row, col, celda)
                        col += 1
                row+=1

            else:
                row+=1
                if tw.rowCount()-1<=row:
                    tw.insertRow(tw.rowCount()-1)
                cb = QComboBox(tw)
                tw.setCellWidget(row, 0, cb)
                insertarDatos(cb,Cond_Comp)
                tw.cellWidget(row, 0).setCurrentText(fila[0])
                font = QtGui.QFont()
                font.setPointSize(12)
                cb.setFont(font)
                tw.resizeColumnToContents(0)
                tw.cellWidget(row, 0).setEnabled(False)

                col=1
                for i in fila:
                    if i=='0.00':
                        i=""
                    if i!=fila[0]:
                        celda=QTableWidgetItem(i)
                        celda.setFlags(flags)
                        celda.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                        if tw.rowCount()-1<=row:
                            tw.insertRow(tw.rowCount()-1)
                        tw.setItem(row, col, celda)
                        col += 1

    else:

        cb0 = QComboBox(tw)
        tw.setCellWidget(0, 0, cb0)
        insertarDatos(cb0,Cond_Comp1)
        cb0.setCurrentIndex(0)
        font = QtGui.QFont()
        font.setPointSize(12)
        cb0.setFont(font)
        tw.resizeColumnToContents(0)

        item1=QTableWidgetItem(Precio)
        item1.setFlags(flags)
        item1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        tw.setItem(0, 2, item1)

        item2=QTableWidgetItem(Valor)
        item2.setFlags(flags)
        item2.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        tw.setItem(0, 3, item2)

        item3=QTableWidgetItem(Moneda)
        item3.setFlags(flags)
        item3.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        tw.setItem(0, 4, item3)

        item22=QTableWidgetItem(Valor)
        item22.setFlags(flags)
        brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item22.setBackground(brush)
        item22.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        tw.setItem(1, 3, item22)

        item33=QTableWidgetItem(Moneda)
        item33.setFlags(flags)
        brush = QtGui.QBrush(QtGui.QColor(255, 213, 79))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item33.setBackground(brush)
        item33.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        tw.setItem(1, 4, item33)

        cb1 = QComboBox(tw)
        tw.setCellWidget(2, 0, cb1)
        if Tipo_Pedido=='Importaciones':
            insertarDatos(cb1,Cond_Comp2)
            cb1.setCurrentIndex(-1)
            font = QtGui.QFont()
            font.setPointSize(12)
            cb1.setFont(font)
            tw.resizeColumnToContents(0)
            cb1.activated.connect(self.Condicion2)
        else:
            insertarDatos(cb1,Cond_Comp3)
            cb1.setCurrentIndex(-1)
            font = QtGui.QFont()
            font.setPointSize(12)
            cb1.setFont(font)
            tw.resizeColumnToContents(0)
            cb1.activated.connect(self.Condicion3)
