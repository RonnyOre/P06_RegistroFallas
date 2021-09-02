import sys
from datetime import datetime
from Funciones04 import *
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.request

sqlFamilia="SELECT CONCAT(Familia,' - ',Descrip) FROM `TAB_MAT_009_Sub_Familias` WHERE Sub_Fam='00' AND Tipo_catalogo='M'"

class ERP_CALIDAD_P001(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("ERP_PCALIDAD_003.ui",self)

        self.pbGrabar.clicked.connect(self.Grabar)
        self.pbOtra_Familia.clicked.connect(self.OtraFamilia)
        self.pbSalir.clicked.connect(self.Salir)

        self.cbFamilia.activated.connect(self.SubFamilia)
        self.cbSubFamilia.activated.connect(self.CodFalla)

        Familia=consultarSql(sqlFamilia)
        insertarDatos(self.cbFamilia,Familia)
        self.cbFamilia.setCurrentIndex(-1)

    def datosGenerales(self, codSoc, empresa, usuario):
        global Cod_Soc, Nom_Soc, Cod_Usuario
        Cod_Soc = codSoc
        Nom_Soc = empresa
        Cod_Usuario = usuario

        cargarLogo(self.lbLogo_Mp,'multiplay')
        cargarLogo(self.lbLogo_Soc, Cod_Soc)
        cargarIcono(self, 'erp')
        cargarIcono(self.pbSalir, 'salir')
        cargarIcono(self.pbOtra_Familia, 'nuevo')
        cargarIcono(self.pbGrabar, 'grabar')

    def SubFamilia(self):
        global Cod_Familia
        if self.cbFamilia.currentText()!=0:
            texto=self.cbFamilia.currentText()
            Cod_Familia=texto[0:texto.find("-")-1]
            if len(Cod_Familia)!=0:
                sqlSubFamilia="SELECT CONCAT(Sub_Fam,' - ',Descrip) FROM `TAB_MAT_009_Sub_Familias` WHERE Familia='%s' AND Sub_Fam!='00' AND Tipo_catalogo='M'"%(Cod_Familia)
                SubFamilia=consultarSql(sqlSubFamilia)
                insertarDatos(self.cbSubFamilia,SubFamilia)
                self.cbSubFamilia.setCurrentIndex(-1)

    def CodFalla(self):
        global Cod_SubFamilia
        if self.cbSubFamilia.currentText()!=0:
            texto=self.cbSubFamilia.currentText()
            Cod_SubFamilia=texto[0:texto.find("-")-1]

    def Grabar(self):
        try:
            Cod_Falla=self.leCod_Falla.text()
            Descrip_Falla=self.pteDescrip_Falla.toPlainText()
            # Descrip_Falla=self.pteDescrip_Falla.setPlainText()
            Estado='1'
            Fecha=datetime.now().strftime("%Y-%m-%d")
            Hora=datetime.now().strftime("%H:%M:%S.%f")

            if len(Cod_Falla) and len(Cod_Familia) and len(Cod_SubFamilia) and len(Descrip_Falla)!=0:
                sql ='''INSERT INTO TAB_ALM_07A_Maestra_Fallas_de_Calidad(Cod_Emp, Cod_Fam, Cod_SubFam, Cod_Falla, Desc_Falla,Estado, Fecha_Reg, Hora_Reg, Usuario_Reg) VALUES  ('%s','%s','%s','%s','%s','%s','%s','%s','%s')''' % (Cod_Soc,Cod_Familia,Cod_SubFamilia,Cod_Falla,Descrip_Falla,Estado,Fecha,Hora,Cod_Usuario)
                respuesta=ejecutarSql(sql)
                if respuesta['respuesta']=='correcto':
                    mensajeDialogo("informacion", "Información", "Registro guardado")
                    self.cbFamilia.setEnabled(False)
                    self.cbFamilia.setStyleSheet("color: rgb(0,0,0);\n""background-color: rgb(255,255,255);")
                    self.leCod_Falla.clear()
                    self.pteDescrip_Falla.clear()

                elif respuesta['respuesta']=='incorrecto':
                    mensajeDialogo("error", "Error", "El registro ya existe")
            else:
                mensajeDialogo("error", "Error", "Faltan llenar datos")
        except:
            mensajeDialogo("error", "Error", "Faltan llenar todos los datos")

    def OtraFamilia(self):
        self.cbFamilia.setEnabled(True)
        self.cbSubFamilia.setEnabled(True)
        self.cbFamilia.setCurrentIndex(-1)
        self.cbSubFamilia.setCurrentIndex(-1)
        self.leCod_Falla.clear()
        self.pteDescrip_Falla.clear()
        self.pbGrabar.setEnabled(True)
        self.pteDescrip_Falla.setEnabled(True)

    def Salir(self):
        self.close()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    _main=ERP_CALIDAD_P001()
    _main.showMaximized()
    app.exec_()
