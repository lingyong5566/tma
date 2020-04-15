class Medication:
    def __init__(self, code, name, maximumDosageAllowedPerKg, dosageLimit, rateType):
        self._code = code
        self._name = name
        self._maximumDosageAllowedPerKg = float(maximumDosageAllowedPerKg)
        self._dosageLimit = float(dosageLimit)
        self._rateType = int(rateType)
    
    @property
    def code(self): #code of medication
        return self._code
    @property
    def name(self): #name of medication
        return self._name
    @property
    def maximumDosageAllowedPerKg(self):
        return self._maximumDosageAllowedPerKg
    @maximumDosageAllowedPerKg.setter
    def maximumDosageAllowedPerKg(self, newMaxDosagePerKg):
        self._maximumDosageAllowedPerKg = newMaxDosagePerKg
    @property
    def dosageLimit(self): #dosage limit of medication
        return self._dosageLimit
    @property
    def rateType(self): #rate type of medication
        return self._rateType
    
    @staticmethod
    def compareByMedicationCode(item):
        return item.code
    
    def recommendedDosage(self, age, weight):
        '''cannot exceed dosage limit
        if patient age <= 12, recommendedDosage / 2'''
        recommendedDosage = min(weight * self._maximumDosageAllowedPerKg, self._dosageLimit)
        if age <= 12:
            recommendedDosage = recommendedDosage / 2
        return recommendedDosage
            
    def compareStrength(self, anotherMedication):
        '''smaller dosageLimit is stronger than larger dosageLimit
        if same, return 0'''
        if self._dosageLimit == anotherMedication._dosageLimit:
            return 0
        elif self._dosageLimit < anotherMedication._dosageLimit:
            #print("{} is stronger than {}".format(self._code, anotherMedication._code))
            return 1
        else:
            #print("{} is stronger than {}".format(anotherMedication._code, self._code))
            return -1
    
    def __str__(self):
        return "{} {}\tMax dose/kg: {}mg\tDose Limit: {}mg\tRate type: {}"\
            .format(self._code, self._name, self._maximumDosageAllowedPerKg, self._dosageLimit, self._rateType)


class PrescribedItem:
    def __init__(self, medication, dosage, frequencyPerDay, duration):
        self._medication = medication
        self._dosage = float(dosage)
        self._frequencyPerDay = int(frequencyPerDay)
        self._duration = int(duration)
    
    @property
    def medication(self): #returns med prescribed
        return self._medication
    @property
    def medicationRateType(self):
        return self._medication.rateType #returns rate type of med
    @property
    def medicationCode(self):
        return self._medication.code #returns code of med
    @property
    def dosage(self): #returns dosage of prescribed med
        return self._dosage
    @property
    def duration(self):
        return self._duration #returns duration of the prescribed med
    @property
    def frequencyPerDay(self): #returns freq per day of prescribed med
        return self._frequencyPerDay
    
    def quantityDispensed(self):
        '''product of dosage, freqPerDay, duration'''
        quantityDispensed = self._dosage *  self._frequencyPerDay * self._duration
        return quantityDispensed
    
    def dosageStrength(self):
        '''quotient from dividing dosage by dosage limit'''
        dosageStrength = self._dosage // self._medication.dosageLimit 
        return dosageStrength
    
    def __str__(self):
        return "{}\n\t{}mg dispensed at {}mg {} times per day for {} days"\
            .format(self._medication.__str__(), self.quantityDispensed(), self._dosage, self._frequencyPerDay, self._duration) 
        
        
class Clinic:
    def __init__(self, medicationList):
        self._medicationList = {} #dictionary of medication
        
    def searchMedicationByCode(self, code):
        '''returns medication with code
        returns None if no medication with code'''
        if code in self._medicationList.keys():
            return self._medicationList[code]
        else:
            return None
    
    def addMedication(self, medication):
        '''adds if medication to dict if code of medication does not contain med code
        returns True if parameter is added
        returns False otherwise'''
        if medication.code not in self._medicationList.keys():
            self._medicationList[medication.code] = medication
            return True
        else:
            return False
    
    def medicationStr(self):
        ''' returns dictionary of medication as a string, sorted according to code'''
        medStr = ""
        medList = list(self._medicationList.values())
        medList.sort(key = Medication.compareByMedicationCode)
        for m in medList:
            medStr += '{}\n'.format(m)
        return medStr
         
class AgeLimitedMedication(Medication):
    '''models one medication that has an age limitation.
    Underage patients should not be prescribed the medicaiton.
    this is a subclass of the Medication class
    '''
    def __init__(self, code, name, maximumDosageAllowedPerKg, dosageLimit, rateType, minimumAge):
        super().__init__(code, name, maximumDosageAllowedPerKg, dosageLimit, rateType)
        self._minimumAge = minimumAge
    
    @property
    def minimumAge(self):
        return self._minimumAge
    @minimumAge.getter
    def minimumAge(self, newMinimumAge):
        self._minimumAge = newMinimumAge
    
    def recommendedDosage(self, age, weight):
        '''if age < minimum age, returns 0
        otherwise, same method as in Medication class, returns recommended dosage'''
        if age < self._minimumAge:
            return 0
        else:
            recommendedDosage = super().recommendedDosage(age, weight)
            return recommendedDosage
    
    def __str__(self):
        return super().__str__()+" Min. age: {} years".format(self._minimumAge)


from datetime import date
from abc import ABC, abstractmethod 
class Visit(ABC):
    '''models one visit to the clinic. This is an abstract class.'''
    _consultRate = 35 #applies to all visits
    _nextId = 1 #starts from 1
    
    def __init__(self, visitDate, patientWeight):
        self._visitId = Visit._nextId
        Visit._nextId += 1 #auto generates running numbers for all visit id of all visits
        self._visitDate = visitDate
        self._patientWeight = float(patientWeight)
        self._prescribedItemList = []
        self._total = 0 #total cost of visit at time of visit; starts with value 0
        #totalCost = consult rate + cost of each prescribed item
    
    @classmethod
    def getConsultRate(cls):
        return cls._consultRate
    @classmethod
    def setConsultRate(cls, newConsultRate):
        cls._consultRate = newConsultRate
    @property
    def visitId(self):
        return self._visitId
    @property
    def visitDate(self):
        return self._visitDate
    @property
    def patientWeight(self):
        return self._patientWeight
    @property
    def total(self):
        return self._total
    
    def searchPrescribedItem(self, code):
        ''' returns prescribed item with parameter code,
        returns None if no prescribed item with the code'''
        for prescribedItem in self._prescribedItemList:
            if prescribedItem.medication.code == code:
                print('prescribedItem found')
                return prescribedItem
        print('no such prescribedItem found')
        return None
            
    def addPrescribedItem(self, prescribedItem):
        ''' if list does not already contain a prescribedItem with the same code,
        adds the parameter prescribedItem to the list of prescribed items list;
        returns True if added
        otherwise False'''
        for item in self._prescribedItemList:
            if item.medication.code == prescribedItem.medication.code:
                return False
        self._prescribedItemList.append(prescribedItem)
        return True

    def removePrescribedItem(self, code):
        '''if the list contains a prescribedItem with the same code,
        removes a prescribedItem with the parameter code from the prescribed list;
        returns True if removed
        otherwise False'''
        if self.searchPrescribedItem(code) != None:
            self._prescribedItemList.remove(self.searchPrescribedItem(code))
            return True
        else:
            return False
    
    def prescribedItemListStr(self):
        '''returns the list of prescribed items as a string, 
        with each medication string on one line, sorted according to code'''
        pstr = ""
        for p in self._prescribedItemList:
            pstr += p.__str__() +'\n'
        return pstr
    
    @abstractmethod
    def getRatePerPrescriptionItem(self, rateType):
        '''method returns the cost of 1 mg of medication given its rate type. 
        This is an abstract method, the cost for 1 mg of medication depends on the type of visit'''
        pass
    
    '''returns sum of cost of prescribed items in the prescribed item list;
    cost of 1mg of med is obtained through calling getRatePerPrescriptionItem method
    and the quantity of medication dispensed''' 
    def getPrescriptionCost(self):
        cost = 0
        for item in self._prescribedItemList:
            cost += item.quantityDispensed() * self.getRatePerPrescriptionItem(item.medication.rateType)
        return cost
        
        
    '''sets the total of the visit
    to the sum of the cost of consultation
    and the prescriptionCost
    method should be called at the end of the visit during payment'''  
    def setTotal(self):
        self._total = self._consultRate + self.getPrescriptionCost()
    
    def __str__(self):
        return ("Id: " + str(self.visitId) + "\t" + str(self.visitDate.strftime(" %a, %d %b %Y ")) + "@" + str(self.patientWeight) + "kg\tTotal: ${:03.2f}" + "\n"\
                 + self.prescribedItemListStr()).format(self.total)



class CorporateVisit(Visit):#sub-class of Visit
    '''visit made by a patient with a company that has selected the clinic as a panel clinic'''
    _consultRate = 20
    
    def __init__(self, visitDate, patientWeight, companyRef):
        super().__init__(visitDate, patientWeight)
        self._companyRef = companyRef #the reference of the company the visit is under
        super().setConsultRate(CorporateVisit._consultRate)
        
    def getRatePerPrescriptionItem(self, rateType):
        '''returns the cost of 1mg of medication given its rate type'''
        if rateType in range(1,3+1):
            return rateType * 0.1
        elif rateType < 0:
            return("Invalid rate type.")
        else:
            return rateType * 0.075
     
    def __str__(self):
#         return (super().__str__())
        return ("Id: " + str(self.visitId) + "\t" + str(self.visitDate.strftime(" %a, %d %b %Y ")) + "@" + str(self.patientWeight) + "kg\tTotal: ${:03.2f} Company:" + str(self._companyRef)+ \
                "\n" + self.prescribedItemListStr()).format(self.total)

        
    

class PrivateVisit(Visit): #sub-class of Visit
    '''the visit made by a patient not attached to any company that has selected the clinic as a panel clinic'''
    
    def getRatePerPrescriptionItem(self, rateType):
        '''returns the cost of 1 mg of medication (rate type of medication * 0.1)'''
        return rateType * 0.1
    
    
    
    

def main():
    #Medication(code, name, maximumDosageAllowedPerKg, dosageLimit, rateType)
    CP12 = Medication('CP12', 'Chloro-6 pheniramine-X', 0.08, 4.0, 3)
    DM01 = Medication('DM01', 'Dex-2 trimethorphan-0', 0.25, 15.0, 2)
    LH03 = Medication('LH03', 'Lyso-X Hydrochloride', 1.00, 10.0, 1)
    print(CP12)
    print(DM01)
    
    #q1a
    print(LH03) #q1(iii) 
    #LH03.maximumDosageAllowedPerKg = 0.8 #q1(iv)
    print(LH03.maximumDosageAllowedPerKg) #q1(iv)
    print(CP12.recommendedDosage(10, 28.2)) #q(v)
    print(DM01.recommendedDosage(30, 52.3)) #q(v)
    print(CP12.compareStrength(DM01)) #q(vi)
    
    #PrescribedItem(medication, dosage, frequencyPerDay, duration)
    #q1b
    p1 = PrescribedItem(CP12, 10, 3, 5) #q1b(ii)
    print(p1.medicationCode) #q1b(iii)
    print(p1.quantityDispensed()) #q1b(iv)
    print(p1.dosageStrength()) #q1b(iv)
    

    #q1c
    c = Clinic('Clinic') #q1c(i)
    c.addMedication(LH03) #q1c(ii)
    c.addMedication(CP12) #q1c(ii)
    c.addMedication(DM01) #q1c(ii)
    
    print(c.addMedication(LH03)) #q1c(iii)
    print(c.medicationStr()) #q1c(iv)
    
    #q2a
    #AgeLimitedMedication(code, name, maximumDosageAllowedPerKg, dosageLimit, rateType, minimumAge)
    ZE01 = AgeLimitedMedication('ZE01', 'Zoledra-Enic1', 0.08, 4.0, 4, 16)
    print(ZE01) #q2a(ii)
    print(ZE01.code) #q2a(iii)
    print(ZE01.name) #q2a(iii)
    ZE01.maximumDosageAllowedPerKg = 0.05 #q2a(iv)
    print(ZE01.maximumDosageAllowedPerKg) #q2a(iv)
    
    #q2b 2c
    #Visit(visitDate, patientWeight)
    #CorporateVisit(visitDate, patientWeight, companyRef)
    p1 = PrescribedItem(DM01, 10.0, 3, 5)
    p2 = PrescribedItem(ZE01, 4.0, 3, 5)
    cv1 = CorporateVisit(date(2020, 1, 20), 65.5, 'C0123')
    pv1 = PrivateVisit(date(2020,3,20), 65.5)
    
    cv1.addPrescribedItem(p1)
    cv1.addPrescribedItem(p2)
    pv1.addPrescribedItem(p1)
    pv1.addPrescribedItem(p2)
    
    cv1.setTotal()
    pv1.setTotal()
    
    print(cv1)
    print(pv1)
    
    
    
    
#if __name__ == '__main__':
main()
