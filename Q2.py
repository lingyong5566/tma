from abc import ABC, abstractmethod
import datetime


class Medication:
    def __init__(self, code, name, maximumDosageAllowedPerKg, dosageLimit, rateType):
        self._code = code
        self._name = name
        self._maximumDosageAllowedPerKg = float(maximumDosageAllowedPerKg)
        self._dosageLimit = float(dosageLimit)
        self._rateType = int(rateType)

    @property
    def code(self):  # code of medication
        return self._code

    @property
    def name(self):  # name of medication
        return self._name

    def maximumDosageAllowedPerKg(self, newMaximumDosageAllowedPerKg=None):
        if newMaximumDosageAllowedPerKg is not None:
            self._maximumDosageAllowedPerKg = newMaximumDosageAllowedPerKg
        else:
            return self._maximumDosageAllowedPerKg

    @property
    def dosageLimit(self):  # dosage limit of medication
        return self._dosageLimit

    @property
    def rateType(self):  # rate type of medication
        return self._rateType

    @staticmethod
    def compareByMedicationCode(item):
        return item.code

    def recommendedDosage(self, age, weight):
        '''cannot exceed dosage limit
        if patient age <= 12, recommendedDosage / 2'''
        recommendedDosage = min(
            weight * self._maximumDosageAllowedPerKg, self._dosageLimit)
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
    def medication(self):  # returns med prescribed
        return self._medication

    @property
    def medicationRateType(self):
        return self._medication.rateType  # returns rate type of med

    @property
    def medicationCode(self):
        return self._medication.code  # returns code of med

    @property
    def dosage(self):  # returns dosage of prescribed med
        return self._dosage

    @property
    def duration(self):
        return self._duration  # returns duration of the prescribed med

    @property
    def frequencyPerDay(self):  # returns freq per day of prescribed med
        return self._frequencyPerDay

    def quantityDispensed(self):
        '''product of dosage, freqPerDay, duration'''
        quantityDispensed = self._dosage * self._frequencyPerDay * self._duration
        return quantityDispensed

    def dosageStrength(self):
        '''quotient from dividing dosage by dosage limit'''
        dosageStrength = self._dosage // self._medication.dosageLimit
        return dosageStrength

    def __str__(self):
        return "{}\n{}mg dispensed at {}mg {} times per day for {} days"\
            .format(self._medication.__str__(), self.quantityDispensed(), self._dosage, self._frequencyPerDay, self._duration)


class Clinic:
    def __init__(self, medicationList):
        self._medicationList = {}  # dictionary of medication

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
        medList.sort(key=Medication.compareByMedicationCode)
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


class Visit(ABC):
    _nextId = 1
    _consultRate = 35

    def __init__(self, visitDate, patientWeight):
        # Variables
        self._visitId = Visit._nextId
        self._visitDate = visitDate
        self._patientWeight = patientWeight
        self._prescribedItemList = []
        self._total = 0
        Visit._nextId += 1

    def getConsultRate(cls):
        return cls._consultRate

    def setConsultRate(cls, newConsultRate):
        cls._consultRate = newConsultRate

    def visitId(self):
        return self._visitId

    def visitDate(self):
        return self._visitDate

    def patientWeight(self):
        return self._patientWeight

    def total(self):
        return self._total

    def searchPrescribedItem(self, code):
        for prescribedItem in self._prescribedItemList:
            if prescribedItem.medication.code == code:
                return prescribedItem
        return None

    def addPrescribedItem(self, prescribedItem):
        for item in self._prescribedItemList:
            if item.medication.code == prescribedItem.medication.code:
                return False
        self._prescribedItemList.append(prescribedItem)
        return True

    def removePrescribedItem(self, code):
        for prescribedItem in self._prescribedItemList:
            for index in prescribedItem:
                if prescribedItem.medication.code == code:
                    del self._prescribedItemList[index]
                    return True
        return False

    def prescribedItemListStr(self):
        st = ""
        for prescribedItem in self._prescribedItemList:
            st += str(prescribedItem) + "\n"
        return st

    def getRatePerPrescriptionItem(self, rateType):
        pass

    def getPrescriptionCost(self):
      cost = 0
      for item in self._prescribedItemList:
            cost += item.quantityDispensed() * self.getRatePerPrescriptionItem(item.medication.rateType)
      return cost

    def setTotal(self):
            self._total = self._consultRate + self.getPrescriptionCost()

    def __str__(self):
        return ("Id: " + str(self.visitId()) + "\t " + str(self.visitDate().strftime("%a  %d %b %Y")) + "\t@" + str(self.patientWeight()) + "kg\tTotal: ${:03.2f}" + "\n" + self.prescribedItemListStr()).format(self.total())

# 2ci


class CorporateVisit(Visit):
    _consultRate = 20

    def __init__(self, visitDate, patientWeight, companyRef):
        self._companyRef = companyRef
        super().__init__(visitDate, patientWeight)
        super().setConsultRate(CorporateVisit._consultRate)

    def getRatePerPrescriptionItem(self, rateType):
        if rateType <= 3 and rateType >= 1:
            return rateType * 0.1
        elif rateType > 3:
            return rateType * 0.075
        else:
            return 0

    def __str__(self):
        return super().__str__()

# 2cii


class PrivateVisit(Visit):
    def __init__(self, visitDate, patientWeight):
        super().__init__(visitDate, patientWeight)
        super().setConsultRate(PrivateVisit._consultRate)

    def getRatePerPrescriptionItem(self, rateType):
        return rateType * 0.1

    def __str__(self):
        return super().__str__()


def main():
    ZE01 = AgeLimitedMedication('ZE01', 'Zoledra-Enic1', 0.08, 4.0, 4, 16)
    print(ZE01)

    # q2a(iii)
    print(ZE01.code)
    print(ZE01.name)

    # q2a(iv)
    ZE01.maximumDosageAllowedPerKg = 0.05
    print(ZE01.maximumDosageAllowedPerKg)

    # 2ciii
    DM01 = Medication('DM01', 'Dex-2 trimethorphan-0', 0.25, 15, 2)

    corpVisit = CorporateVisit(datetime.date(2020, 1, 20), 65.5, "C0123")
    privVisit = PrivateVisit(datetime.date(2020, 3, 20), 65.5)

    PI1 = PrescribedItem(DM01, 10, 3, 5)
    PI2 = PrescribedItem(ZE01, 4, 3, 5)

    corpVisit.addPrescribedItem(PI1)
    corpVisit.addPrescribedItem(PI2)

    privVisit.addPrescribedItem(PI1)
    privVisit.addPrescribedItem(PI2)

    corpVisit.setTotal()
    privVisit.setTotal()

    print(corpVisit)
    print(privVisit)


main()
console.log("from abc import ABC, abstractmethod
import datetime


class Medication:
    def __init__(self, code, name, maximumDosageAllowedPerKg, dosageLimit, rateType):
        self._code = code
        self._name = name
        self._maximumDosageAllowedPerKg = float(maximumDosageAllowedPerKg)
        self._dosageLimit = float(dosageLimit)
        self._rateType = int(rateType)

    @property
    def code(self):  # code of medication
        return self._code

    @property
    def name(self):  # name of medication
        return self._name

    def maximumDosageAllowedPerKg(self, newMaximumDosageAllowedPerKg=None):
        if newMaximumDosageAllowedPerKg is not None:
            self._maximumDosageAllowedPerKg = newMaximumDosageAllowedPerKg
        else:
            return self._maximumDosageAllowedPerKg

    @property
    def dosageLimit(self):  # dosage limit of medication
        return self._dosageLimit

    @property
    def rateType(self):  # rate type of medication
        return self._rateType

    @staticmethod
    def compareByMedicationCode(item):
        return item.code

    def recommendedDosage(self, age, weight):
        '''cannot exceed dosage limit
        if patient age <= 12, recommendedDosage / 2'''
        recommendedDosage = min(
            weight * self._maximumDosageAllowedPerKg, self._dosageLimit)
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
    def medication(self):  # returns med prescribed
        return self._medication

    @property
    def medicationRateType(self):
        return self._medication.rateType  # returns rate type of med

    @property
    def medicationCode(self):
        return self._medication.code  # returns code of med

    @property
    def dosage(self):  # returns dosage of prescribed med
        return self._dosage

    @property
    def duration(self):
        return self._duration  # returns duration of the prescribed med

    @property
    def frequencyPerDay(self):  # returns freq per day of prescribed med
        return self._frequencyPerDay

    def quantityDispensed(self):
        '''product of dosage, freqPerDay, duration'''
        quantityDispensed = self._dosage * self._frequencyPerDay * self._duration
        return quantityDispensed

    def dosageStrength(self):
        '''quotient from dividing dosage by dosage limit'''
        dosageStrength = self._dosage // self._medication.dosageLimit
        return dosageStrength

    def __str__(self):
        return "{}\n{}mg dispensed at {}mg {} times per day for {} days"\
            .format(self._medication.__str__(), self.quantityDispensed(), self._dosage, self._frequencyPerDay, self._duration)


class Clinic:
    def __init__(self, medicationList):
        self._medicationList = {}  # dictionary of medication

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
        medList.sort(key=Medication.compareByMedicationCode)
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


class Visit(ABC):
    _nextId = 1
    _consultRate = 35

    def __init__(self, visitDate, patientWeight):
        # Variables
        self._visitId = Visit._nextId
        self._visitDate = visitDate
        self._patientWeight = patientWeight
        self._prescribedItemList = []
        self._total = 0
        Visit._nextId += 1

    def getConsultRate(cls):
        return cls._consultRate

    def setConsultRate(cls, newConsultRate):
        cls._consultRate = newConsultRate

    def visitId(self):
        return self._visitId

    def visitDate(self):
        return self._visitDate

    def patientWeight(self):
        return self._patientWeight

    def total(self):
        return self._total

    def searchPrescribedItem(self, code):
        for prescribedItem in self._prescribedItemList:
            if prescribedItem.medication.code == code:
                return prescribedItem
        return None

    def addPrescribedItem(self, prescribedItem):
        for item in self._prescribedItemList:
            if item.medication.code == prescribedItem.medication.code:
                return False
        self._prescribedItemList.append(prescribedItem)
        return True

    def removePrescribedItem(self, code):
        for prescribedItem in self._prescribedItemList:
            for index in prescribedItem:
                if prescribedItem.medication.code == code:
                    del self._prescribedItemList[index]
                    return True
        return False

    def prescribedItemListStr(self):
        st = ""
        for prescribedItem in self._prescribedItemList:
            st += str(prescribedItem) + "\n"
        return st

    def getRatePerPrescriptionItem(self, rateType):
        pass

      def getPrescriptionCost(self):
            cost = 0
            for item in self._prescribedItemList:
                  cost += item.quantityDispensed() * self.getRatePerPrescriptionItem(item.medication.rateType)
            return cost

      def setTotal(self):
            self._total = self._consultRate + self.getPrescriptionCost()

    def __str__(self):
        return ("Id: " + str(self.visitId()) + "\t " + str(self.visitDate().strftime("%a  %d %b %Y")) + "\t@" + str(self.patientWeight()) + "kg\tTotal: ${:03.2f}" + "\n" + self.prescribedItemListStr()).format(self.total())

# 2ci


class CorporateVisit(Visit):
    _consultRate = 20

    def __init__(self, visitDate, patientWeight, companyRef):
        self._companyRef = companyRef
        super().__init__(visitDate, patientWeight)
        super().setConsultRate(CorporateVisit._consultRate)

    def getRatePerPrescriptionItem(self, rateType):
        if rateType <= 3 and rateType >= 1:
            return rateType * 0.1
        elif rateType > 3:
            return rateType * 0.075
        else:
            return 0

    def getPrescriptionCost(self):
        cost = 0
        for item in self._prescribedItemList:
            cost += item.quantityDispensed() * self.getRatePerPrescriptionItem(item.medication.rateType)
        return cost

    def setTotal(self):
        self._total = self._consultRate + self.getPrescriptionCost()

    def __str__(self):
        return super().__str__()

# 2cii


class PrivateVisit(Visit):
    def __init__(self, visitDate, patientWeight):
        super().__init__(visitDate, patientWeight)
        super().setConsultRate(PrivateVisit._consultRate)

    def getRatePerPrescriptionItem(self, rateType):
        return rateType * 0.1

    def __str__(self):
        return super().__str__()


def main():
    ZE01 = AgeLimitedMedication('ZE01', 'Zoledra-Enic1', 0.08, 4.0, 4, 16)
    print(ZE01)

    # q2a(iii)
    print(ZE01.code)
    print(ZE01.name)

    # q2a(iv)
    ZE01.maximumDosageAllowedPerKg = 0.05
    print(ZE01.maximumDosageAllowedPerKg)

    # 2ciii
    DM01 = Medication('DM01', 'Dex-2 trimethorphan-0', 0.25, 15, 2)

    corpVisit = CorporateVisit(datetime.date(2020, 1, 20), 65.5, "C0123")
    privVisit = PrivateVisit(datetime.date(2020, 3, 20), 65.5)

    PI1 = PrescribedItem(DM01, 10, 3, 5)
    PI2 = PrescribedItem(ZE01, 4, 3, 5)

    corpVisit.addPrescribedItem(PI1)
    corpVisit.addPrescribedItem(PI2)

    privVisit.addPrescribedItem(PI1)
    privVisit.addPrescribedItem(PI2)

    corpVisit.setTotal()
    privVisit.setTotal()

    print(corpVisit)
    print(privVisit)


main()
", from abc import ABC, abstractmethod
import datetime


class Medication:
    def __init__(self, code, name, maximumDosageAllowedPerKg, dosageLimit, rateType):
        self._code = code
        self._name = name
        self._maximumDosageAllowedPerKg = float(maximumDosageAllowedPerKg)
        self._dosageLimit = float(dosageLimit)
        self._rateType = int(rateType)

    @property
    def code(self):  # code of medication
        return self._code

    @property
    def name(self):  # name of medication
        return self._name

    def maximumDosageAllowedPerKg(self, newMaximumDosageAllowedPerKg=None):
        if newMaximumDosageAllowedPerKg is not None:
            self._maximumDosageAllowedPerKg = newMaximumDosageAllowedPerKg
        else:
            return self._maximumDosageAllowedPerKg

    @property
    def dosageLimit(self):  # dosage limit of medication
        return self._dosageLimit

    @property
    def rateType(self):  # rate type of medication
        return self._rateType

    @staticmethod
    def compareByMedicationCode(item):
        return item.code

    def recommendedDosage(self, age, weight):
        '''cannot exceed dosage limit
        if patient age <= 12, recommendedDosage / 2'''
        recommendedDosage = min(
            weight * self._maximumDosageAllowedPerKg, self._dosageLimit)
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
    def medication(self):  # returns med prescribed
        return self._medication

    @property
    def medicationRateType(self):
        return self._medication.rateType  # returns rate type of med

    @property
    def medicationCode(self):
        return self._medication.code  # returns code of med

    @property
    def dosage(self):  # returns dosage of prescribed med
        return self._dosage

    @property
    def duration(self):
        return self._duration  # returns duration of the prescribed med

    @property
    def frequencyPerDay(self):  # returns freq per day of prescribed med
        return self._frequencyPerDay

    def quantityDispensed(self):
        '''product of dosage, freqPerDay, duration'''
        quantityDispensed = self._dosage * self._frequencyPerDay * self._duration
        return quantityDispensed

    def dosageStrength(self):
        '''quotient from dividing dosage by dosage limit'''
        dosageStrength = self._dosage // self._medication.dosageLimit
        return dosageStrength

    def __str__(self):
        return "{}\n{}mg dispensed at {}mg {} times per day for {} days"\
            .format(self._medication.__str__(), self.quantityDispensed(), self._dosage, self._frequencyPerDay, self._duration)


class Clinic:
    def __init__(self, medicationList):
        self._medicationList = {}  # dictionary of medication

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
        medList.sort(key=Medication.compareByMedicationCode)
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


class Visit(ABC):
    _nextId = 1
    _consultRate = 35

    def __init__(self, visitDate, patientWeight):
        # Variables
        self._visitId = Visit._nextId
        self._visitDate = visitDate
        self._patientWeight = patientWeight
        self._prescribedItemList = []
        self._total = 0
        Visit._nextId += 1

    def getConsultRate(cls):
        return cls._consultRate

    def setConsultRate(cls, newConsultRate):
        cls._consultRate = newConsultRate

    def visitId(self):
        return self._visitId

    def visitDate(self):
        return self._visitDate

    def patientWeight(self):
        return self._patientWeight

    def total(self):
        return self._total

    def searchPrescribedItem(self, code):
        for prescribedItem in self._prescribedItemList:
            if prescribedItem.medication.code == code:
                return prescribedItem
        return None

    def addPrescribedItem(self, prescribedItem):
        for item in self._prescribedItemList:
            if item.medication.code == prescribedItem.medication.code:
                return False
        self._prescribedItemList.append(prescribedItem)
        return True

    def removePrescribedItem(self, code):
        for prescribedItem in self._prescribedItemList:
            for index in prescribedItem:
                if prescribedItem.medication.code == code:
                    del self._prescribedItemList[index]
                    return True
        return False

    def prescribedItemListStr(self):
        st = ""
        for prescribedItem in self._prescribedItemList:
            st += str(prescribedItem) + "\n"
        return st

    def getRatePerPrescriptionItem(self, rateType):
        pass

      def getPrescriptionCost(self):
            cost = 0
            for item in self._prescribedItemList:
                  cost += item.quantityDispensed() * self.getRatePerPrescriptionItem(item.medication.rateType)
            return cost

      def setTotal(self):
            self._total = self._consultRate + self.getPrescriptionCost()

    def __str__(self):
        return ("Id: " + str(self.visitId()) + "\t " + str(self.visitDate().strftime("%a  %d %b %Y")) + "\t@" + str(self.patientWeight()) + "kg\tTotal: ${:03.2f}" + "\n" + self.prescribedItemListStr()).format(self.total())

# 2ci


class CorporateVisit(Visit):
    _consultRate = 20

    def __init__(self, visitDate, patientWeight, companyRef):
        self._companyRef = companyRef
        super().__init__(visitDate, patientWeight)
        super().setConsultRate(CorporateVisit._consultRate)

    def getRatePerPrescriptionItem(self, rateType):
        if rateType <= 3 and rateType >= 1:
            return rateType * 0.1
        elif rateType > 3:
            return rateType * 0.075
        else:
            return 0

    def getPrescriptionCost(self):
        cost = 0
        for item in self._prescribedItemList:
            cost += item.quantityDispensed() * self.getRatePerPrescriptionItem(item.medication.rateType)
        return cost

    def setTotal(self):
        self._total = self._consultRate + self.getPrescriptionCost()

    def __str__(self):
        return super().__str__()

# 2cii


class PrivateVisit(Visit):
    def __init__(self, visitDate, patientWeight):
        super().__init__(visitDate, patientWeight)
        super().setConsultRate(PrivateVisit._consultRate)

    def getRatePerPrescriptionItem(self, rateType):
        return rateType * 0.1

    def __str__(self):
        return super().__str__()


def main():
    ZE01 = AgeLimitedMedication('ZE01', 'Zoledra-Enic1', 0.08, 4.0, 4, 16)
    print(ZE01)

    # q2a(iii)
    print(ZE01.code)
    print(ZE01.name)

    # q2a(iv)
    ZE01.maximumDosageAllowedPerKg = 0.05
    print(ZE01.maximumDosageAllowedPerKg)

    # 2ciii
    DM01 = Medication('DM01', 'Dex-2 trimethorphan-0', 0.25, 15, 2)

    corpVisit = CorporateVisit(datetime.date(2020, 1, 20), 65.5, "C0123")
    privVisit = PrivateVisit(datetime.date(2020, 3, 20), 65.5)

    PI1 = PrescribedItem(DM01, 10, 3, 5)
    PI2 = PrescribedItem(ZE01, 4, 3, 5)

    corpVisit.addPrescribedItem(PI1)
    corpVisit.addPrescribedItem(PI2)

    privVisit.addPrescribedItem(PI1)
    privVisit.addPrescribedItem(PI2)

    corpVisit.setTotal()
    privVisit.setTotal()

    print(corpVisit)
    print(privVisit)


main()
)
