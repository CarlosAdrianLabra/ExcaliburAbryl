class digitToWord:
    def unit(self, num):
        word = ''
        if(num == "1"):
            word = 'UNO'
        if(num == "2"):
            word = 'DOS'
        if(num == "3"):
            word = 'TRES'
        if(num == "4"):
            word = 'CUATRO'
        if(num == "5"):
            word = 'CINCO'
        if(num == "6"):
            word = 'SEIS'
        if(num == "7"):
            word = 'SIETE'
        if(num == "8"):
            word = 'OCHO'
        if(num == "9"):
            word = 'NUEVE'
        word.strip()
        return word
    
    def tens(self, num):
        word = ''
        if(num[0] == '1'):
            if(num[1] == '0'):
                word = 'DIEZ'
            if(num[1] == '1'):
                word = 'ONCE'
            if(num[1] == '2'):
                word = 'DOCE'
            if(num[1] == '3'):
                word = 'TRECE'
            if(num[1] == '4'):
                word = 'CATORCE'
            if(num[1] == '5'):
                word = 'QUINCE'
            if(num[1] == '6'):
                word = 'DIECISEIS'
            if(num[1] == '7'):
                word = 'DIECISIETE'
            if(num[1] == '8'):
                word = 'DIECIOCHO'
            if(num[1] == '9'):
                word = 'DIECINUEVE'
        elif(num[0] == '2'):
            if(num[1] == '0'):
                word = 'VEINTE'
            if(num[1] == '1'):
                word = 'VEINTIUNO'
            if(num[1] == '2'):
                word = 'VEINTIDOS'
            if(num[1] == '3'):
                word = 'VEINTITRES'
            if(num[1] == '4'):
                word = 'VEINTICUATRO'
            if(num[1] == '5'):
                word = 'VEINTICINCO'
            if(num[1] == '6'):
                word = 'VEINTISEIS'
            if(num[1] == '7'):
                word = 'VEINTISIETE'
            if(num[1] == '8'):
                word = 'VEINTIOCHO'
            if(num[1] == '9'):
                word = 'VEINTINUEVE'
        elif(num[0] == '3'):
            after = self.unit(num[1])
            if(num[1] == '0'):
                word = 'TREINTA'
            if(num[1] != '0'):
                word = 'TREINTA Y'
            word = word + " " + after
            
        elif(num[0] == '4'):
            after = self.unit(num[1])
            if(num[1] == '0'):
                word = 'CUARENTA'
            if(num[1] != '0'):
                word = 'CUARENTA Y'
            word = word + " " + after
            
        elif(num[0] == '5'):
            after = self.unit(num[1])
            if(num[1] == '0'):
                word = 'CINCUENTA'
            if(num[1] != '0'):
                word = 'CINCUENTA Y'
            word = word + " " + after
            
        elif(num[0] == '6'):
            after = self.unit(num[1])
            if(num[1] == '0'):
                word = 'SESENTA'
            if(num[1] != '0'):
                word = 'SESENTA Y'
            word = word + " " + after
            
        elif(num[0] == '7'):
            after = self.unit(num[1])
            if(num[1] == '0'):
                word = 'SETENTA'
            if(num[1] != '0'):
                word = 'SETENTA Y'
            word = word + " " + after
            
        elif(num[0] == '8'):
            after = self.unit(num[1])
            if(num[1] == '0'):
                word = 'OCHENTA'
            if(num[1] != '0'):
                word = 'OCHENTA Y'
            word = word + " " + after
            
        elif(num[0] == '9'):
            after = self.unit(num[1])
            if(num[1] == '0'):
                word = 'NOVENTA'
            if(num[1] != '0'):
                word = 'NOVENTA Y'
            word = word + " " + after
            
        word = word.strip()
        return word

    def hundreds(self, num):
        word = ''
        after = ' ' + self.tens(num[1:])

        if(num[0] == "1"):
            word = 'CIENTO'
        if(num[0] == "1"):
            if (num[1] == '0'):
                if (num[2] == '0'):
                    word = 'CIEN'
        if (num[0] == '1'):
            if (num[1] == '0'):
                if (num[2] == '1'):
                    word = 'CIENTO UNO'
                if (num[2] == '2'):
                    word = 'CIENTO DOS'
                if (num[2] == '3'):
                    word = 'CIENTO TRES'
                if (num[2] == '4'):
                    word = 'CIENTO CUATRO'
                if (num[2] == '5'):
                    word = 'CIENTO CINCO'
                if (num[2] == '6'):
                    word = 'CIENTO SEIS'
                if (num[2] == '7'):
                    word = 'CIENTO SIETE'
                if (num[2] == '8'):
                    word = 'CIENTO OCHO'
                if (num[2] == '9'):
                    word = 'CIENTO NUEVE'
        if(num[0] == "2"):
            word = 'DOSCIENTOS'
        if (num[0] == '2'):
            if (num[1] == '0'):
                after = ' ' + self.unit(num[2:])
        if(num[0] == "3"):
            word = 'TRESCIENTOS'
        if (num[0] == '3'):
            if (num[1] == '0'):
                after = ' ' + self.unit(num[2:])
        if(num[0] == "4"):
            word = 'CUATROCIENTOS'
        if (num[0] == '4'):
            if (num[1] == '0'):
                after = ' ' + self.unit(num[2:])
        if(num[0] == "5"):
            word = 'QUINIENTOS'
        if (num[0] == '5'):
            if (num[1] == '0'):
                after = ' ' + self.unit(num[2:])
        if(num[0] == "6"):
            word = 'SEISCIENTOS'
        if (num[0] == '6'):
            if (num[1] == '0'):
                after = ' ' + self.unit(num[2:])
        if(num[0] == "7"):
            word = 'SETECIENTOS'
        if (num[0] == '7'):
            if (num[1] == '0'):
                after = ' ' + self.unit(num[2:])
        if(num[0] == "8"):
            word = 'OCHOCIENTOS'
        if (num[0] == '8'):
            if (num[1] == '0'):
                after = ' ' + self.unit(num[2:])
        if(num[0] == "9"):
            word = 'NOVECIENTOS'
        if (num[0] == '9'):
            if (num[1] == '0'):
                after = ' ' + self.unit(num[2:])
   
        word = word + after

        word.strip()
        return word
    
    def thousands(self, num):
        word = ''
        after = ' ' + self.hundreds(num[1:])

        if(num[0] == "1"):
            word = 'UN MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    after = ' ' + self.unit(num[3:])
        if(num[0] == "2"):
            word = 'DOS MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    after = ' ' + self.unit(num[3:])      
        if(num[0] == "3"):
            word = 'TRES MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    after = ' ' + self.unit(num[3:])     
        if(num[0] == "4"):
            word = 'CUATRO MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    after = ' ' + self.unit(num[3:])
        if(num[0] == "5"):
            word = 'CINCO MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    after = ' ' + self.unit(num[3:])
        if(num[0] == "6"):
            word = 'SEIS MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    after = ' ' + self.unit(num[3:])
        if(num[0] == "7"):
            word = 'SIETE MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    after = ' ' + self.unit(num[3:])
        if(num[0] == "8"):
            word = 'OCHO MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    after = ' ' + self.unit(num[3:])
        if(num[0] == "9"):
            word = 'NUEVE MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    after = ' ' + self.unit(num[3:])
        
        word = word + after

        word = word.strip()
        return word
    
    def ten_thousands(self, num):
        word = ''
        after = ' ' + self.thousands(num[1:])
        after = ' ' + self.hundreds(num[2:])

        if(num[0] == "1"):
            word = 'DIEZ MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '1'):
                word = 'ONCE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '2'):
                word = 'DOCE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '3'):
                word = 'TRECE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '4'):
                word = 'CATORCE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '5'):
                word = 'QUINCE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '6'):
                word = 'DIECISEIS MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '7'):
                word = 'DIECISIETE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '8'):
                word = 'DIECIOCHO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '9'):
                word = 'DIECINUEVE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
        if(num[0] == "2"):
            word = 'VEINTE MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '1'):
                word = 'VEINTIUN MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '2'):
                word = 'VEINTIDOS MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '3'):
                word = 'VEINTITRES MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '4'):
                word = 'VEINTICUATRO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '5'):
                word = 'VEINTICINCO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '6'):
                word = 'VEINTISEIS MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '7'):
                word = 'VEINTISIETE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '8'):
                word = 'VEINTIOCHO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '9'):
                word = 'VEINTINUEVE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
        if(num[0] == "3"):
            word = 'TREINTA MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '1'):
                word = 'TREINTA Y UN MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '2'):
                word = 'TREINTA Y DOS MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '3'):
                word = 'TREINTA Y TRES MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '4'):
                word = 'TREINTA Y CUATRO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '5'):
                word = 'TREINTA Y CINCO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '6'):
                word = 'TREINTA Y SEIS MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '7'):
                word = 'TREINTA Y SIETE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '8'):
                word = 'TREINTA Y OCHO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '9'):
                word = 'TREINTA Y NUEVE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
        if(num[0] == "4"):
            word = 'CUARENTA MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '1'):
                word = 'CUARENTA Y UN MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '2'):
                word = 'CUARENTA Y DOS MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '3'):
                word = 'CUARENTA Y TRES MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '4'):
                word = 'CUARENTA Y CUATRO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '5'):
                word = 'CUARENTA Y CINCO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '6'):
                word = 'CUARENTA Y SEIS MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '7'):
                word = 'CUARENTA Y SIETE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '8'):
                word = 'CUARENTA Y OCHO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '9'):
                word = 'CUARENTA Y NUEVE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
        if(num[0] == "5"):
            word = 'CINCUENTA MIL'
            if (num[1] == '0'):
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '1'):
                word = 'CINCUENTA Y UN MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '2'):
                word = 'CINCUENTA Y DOS MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '3'):
                word = 'CINCUENTA Y TRES MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '4'):
                word = 'CINCUENTA Y CUATRO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '5'):
                word = 'CINCUENTA Y CINCO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '6'):
                word = 'CINCUENTA Y SEIS MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '7'):
                word = 'CINCUENTA Y SIETE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '8'):
                word = 'CINCUENTA Y OCHO MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])
            if (num[1] == '9'):
                word = 'CINCUENTA Y NUEVE MIL'
                if (num[2] == '0'):
                    if (num[3] == '0'):
                        after = ' ' + self.unit(num[4:])

        word = word + after

        word = word.strip()
        return word
    
def seg(n):
    n = n[::-1]
    a = [n[i:i+5][::-1] for i in range(0,len(n),5)]
    return a

def word(digit):
    if(isinstance(digit, int)):digit=str(digit)
    if(digit.isdigit()):
        digit = digit.lstrip('0')
        word = digitToWord()
        #bm = ["","MIL","MILLON","BILLON","TRILLON"]
        segn = seg(digit)
        response = ''
        b = 0
        
        for i in range(len(segn)):
            if len(segn[i])==1:
                response = word.unit(segn[i]) + ' ' + ' ' + response
            
            if len(segn[i])==2:
                response = word.tens(segn[i]) + ' ' + ' ' + response
            
            if len(segn[i])==3:
                response = word.hundreds(segn[i]) + ' ' + ' ' + response
            
            if len(segn[i])==4:
                response = word.thousands(segn[i]) + ' ' + ' ' + response
            
            if len(segn[i])==5:
                response = word.ten_thousands(segn[i]) + ' ' + ' ' + response

        return response.rstrip(" ")
    else:
        raise Exception('Make sure that, the number you passed "'+str(digit)+'" doesn\'t contain any alphabet or special symbol!')