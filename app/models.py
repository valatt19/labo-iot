from app import db, app
from datetime import datetime

class AdvicesConsumption(db.Model):
    """

    """
    __tablename__ = "adviceConsumption"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_d = db.Column(db.String(150), nullable=False)
    advice = db.Column(db.Text, nullable=False)
    device = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return "TYPE:  %s, \n ADVICE: %s \n DEVICE: %s\n\n" % (self.type, self.advice, self.device)

    def add_new_advice(type_d, advice, device):
        """
        Add a new advice on energy consumption

        :parameter
        type: type of the advice (reduce consumption, new purchase of appliances, tip) (string)
        advice: the advice (string)
        device: kitchen device (fridge, bulb, oven, microwave, ...)

        :return:
         A advice
        """

        new_advice = AdvicesConsumption(type_d=type_d, advice=advice, device=device)
        db.session.add(new_advice)
        db.session.commit()

    def get_type_d(self):
        """
        :return the type of the device (str)
        """
        return self.type_d

    def set_type_d(self, new_type):
        """
        affect: type_d = new_type (str)
        """
        self.type_d = new_type
        db.session.commit()

class Devices(db.Model):
    """

    """
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    nb_volt = db.Column(db.Integer, nullable=False)
    hub_port = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    measures = db.relationship("MeasureConsumption", overlaps="measures")

    def get_between_measures(self, start, end):
        """day_consumption = 0
        begin = datetime.datetime(date.year, date.month, date.day)
        print(begin) 
        print(date)
        with app.app_context():
            mesures = list(MeasureConsumption.query.filter(MeasureConsumption.datetime.between(begin, date)))
            for m in mesures"""
        device_measures = self.measures
        between_measures = []
        for measure in list(device_measures):
            if start <= measure.datetime <= end:
                between_measures.append(measure)

        return between_measures


    def add_new_device(name, description, nb_volt=12, hub_port=0):
        """
        Add a new device

        :parameter
        name: name of the device (string)
        description: description of the device (string)
        """

        new_device = Devices(name=name, nb_volt=nb_volt, hub_port=hub_port, description=description)
        db.session.add(new_device)
        db.session.commit()

class MeasureConsumption(db.Model):
    """
    """
    __tablename__ = "measure_consumption"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    measure = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"))
    device = db.relationship("Devices", backref=db.backref("device", lazy=True), overlaps="measures")

    def add_new_measure(m, did, date = None):
        """
        Add a new device

        :parameter
        measure: name of the device (string)
        device_id: description of the device (string)
        """
        if date is None:
            date=datetime.today()

        with app.app_context():
            new_measure = MeasureConsumption(measure=m, datetime=date, device_id=did)
            db.session.add(new_measure)
            db.session.commit()

    def get_serializable_measure(self):
        return {"datetime":self.datetime.strftime("%Y/%m/%d, %H:%M:%S"), "measure":self.measure}


class WindowLog(db.Model):
    """
    """
    __tablename__ = "window_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def add_new_action(action):
        """
        Add a new action in the log

        :parameter
        measure: name of the device (string)
        device_id: description of the device (string)
        """
        with app.app_context():
            new_action = WindowLog(action=action, datetime=datetime.today())
            db.session.add(new_action)
            db.session.commit()

    def get_serializable_action(self):
        return {"datetime":self.datetime.strftime("%Y/%m/%d, %H:%M:%S"), "action":self.action}


# Initializing the database
with app.app_context():
    db.drop_all()
    db.create_all()

    Devices.query.delete()
    Devices.add_new_device(name="Frigo", description="Frigo de 220V", nb_volt=220, hub_port=0)
    Devices.add_new_device(name="Lave-vaisselle", description="Lave-vaisselle de 22V", nb_volt=120, hub_port=2)
    Devices.add_new_device(name="Lampe", description="Ampoule ??co de 12V", nb_volt=12, hub_port=3)
    Devices.add_new_device(name="Bouilloire", description="Bouiloire de 24V", nb_volt=24, hub_port=-1)
    Devices.add_new_device(name="Taque de cuisson", description="Taque de cuisson ??lectrique", nb_volt=220, hub_port=1)

    AdvicesConsumption.query.delete()
    AdvicesConsumption.add_new_advice("Consommation Ampoule", "Une ampoule ?? incandescence a besoin de 60 W pour donner 750 lumens", "Ampoule ?? incandescence")
    AdvicesConsumption.add_new_advice("Consommation Ampoule", "Une ampoule ??conomique a besoin 12 W pour donner 750 lumens", "Ampoule ??conomique")
    AdvicesConsumption.add_new_advice("Consommation Ampoule", "Une ampoule LED a besoin 6.5 W pour donner 750 lumens", "Ampoule LED")

    AdvicesConsumption.add_new_advice("Consommation Taque", "Energie n??cessaire pour chauffer 1,5 litre d'eau de 20 ?? 95??C = 295 Wh", "Gazette")
    AdvicesConsumption.add_new_advice("Consommation Taque", "Energie n??cessaire pour chauffer 1,5 litre d'eau de 20 ?? 95??C = 162 Wh", "Induction")
    AdvicesConsumption.add_new_advice("Consommation Taque", "Energie n??cessaire pour chauffer 1,5 litre d'eau de 20 ?? 95??C = 233 Wh", "Vitroc??ramique")
    AdvicesConsumption.add_new_advice("Consommation Taque", "Energie n??cessaire pour chauffer 1,5 litre d'eau de 20 ?? 95??C = 252 Wh", "Fonte")
    AdvicesConsumption.add_new_advice("Consommation Taque", "Les taques ?? inductions consomment 30 ?? 40% d'??lectricit?? en moins", "Induction")

    AdvicesConsumption.add_new_advice("Consommation", "Un frigidaire-Cong??lateur A+/304 L consomme 304 kWh par an ==> co??t 46,99 ??? (compteur de 6kVA en option base)", "Frigo")
    AdvicesConsumption.add_new_advice("Consommation", "Un frigidaire-Cong??lateur A++/304 L consomme 257 kWh par an ==> co??t 39,73 ??? (compteur de 6kVA en option base)", "Frigo")
    AdvicesConsumption.add_new_advice("Consommation", "Un frigidaire-Cong??lateur A+++/304 L consomme 160 kWh par an ==> co??t 24,74 ??? (compteur de 6kVA en option base)", "Frigo")

    AdvicesConsumption.add_new_advice("Astuce", "Pour la cuisson ?? ??lectricit?? privil??gier les casseroles ?? fond parfaitement plat", "Cuisson Electrique")
    AdvicesConsumption.add_new_advice("Astuce", "Pour acc??l??er la cuissson ou le chauffage de l'eau vous devriez mettre un couvercle. Je geste"
                                                "peut vous faire ??conomiser 45 ???/an.", "Cuisson")

    AdvicesConsumption.add_new_advice("Astuce", "Si on fait une grande quantit?? de vaisselle mieux vaut utiliser la vaisselle pour ??conomiser de l'eau."
                                                "Une machine peut laver jusqu????? 160 pi??ces de vaisselle avec seulement 10 ?? 12 litres d???eau.", "Lave-vaisselle")
    AdvicesConsumption.add_new_advice("Astuce", "Si vous devez rincer la vaisselle avant de la mettre dans la machine utiliser, utiliser de l'eau qui "
                                                "a d??j?? servi par exemple ?? laver les l??gumes ou cuir les p??tes...", "Lave-vaisselle")
    AdvicesConsumption.add_new_advice("Astuce", "Bien remplir le lave-vaisselle et consulter le mode d???emploi pour conna??tre la consommation d'eau et d'??nergie de chaque programme"
                                        , "Lave-vaisselle")

    AdvicesConsumption.add_new_advice("Astuce", "D??givrer le frigidaire peut vous faire ??conomiser de l'argent. Par exemple de 2 mm de givre c'est environ 10 % de consommation"
                                                " suppl??mentaire et 5 mm de givre c'est + 30% de consommation.", "Frigidaire")
    AdvicesConsumption.add_new_advice("Astuce", "Bien choisir l'emplacement de son frigidaire: ne pas le mettre trop pr??s des radiateurs, de la chaudi??re ou du four puisqu'ils"
                                                " produisent de la chaleur et auront plus tendances ?? le faire fonctionner d'avantage.", "Frigidaire")
    AdvicesConsumption.add_new_advice("Astuce", "Choisir la temp??rature adequate pour la conservation afin d'??conomiser de l'argent. 4-5?? pour le r??frig??rateur et -18?? pour la cong??lation", "Frigidaire")

    AdvicesConsumption.add_new_advice("Astuce", "Quand on est raccord?? au gaz, cuisiner avec ce derneir co??te moiti?? moins ch??re que"
                                                "l'??lectrique car on utilise le gaz pour se chauffer", "Choix ??nergie")
    AdvicesConsumption.add_new_advice("Astuce", "A??rez suffisament votre cuisine si vous utiliser le gaz et utiliser la hotte ?? chaque cuisson", "Utilisation gaz")
    AdvicesConsumption.add_new_advice("Astuce", "Si on utilise l'??lectricit?? il faut privil??gier les taques ?? induction car elle "
                                                "consomme 30 ?? 40 % d?????lectricit?? en moins que les taques en fonte ou les vitroc??ramiques.", "Choix ??nergie")

    AdvicesConsumption.add_new_advice("Achat G", "Bien r??fl??chire ?? ses habitudes afin de prendre l'appareil le mieux "
                                                "adapt?? ?? ses besoins et ?? la taille de sa famille", "Achat")
    AdvicesConsumption.add_new_advice("Achat G", "Le froid alimentaire repr??sente 26% de la facture d'??l??ctricit?? d'apr??s EDF.", "Frigo")
    AdvicesConsumption.add_new_advice("Achat G", "Prendre au serieux l'??tiquette d'??nergie car entre un mod??le A+ et A+++ "
                                                "la consommation peut varier du simple au double", "Achat")


    AdvicesConsumption.add_new_advice("Utilisation", "Pour l'induction utiliser des ustenciles ?? adapt??s (au fond aimant??)", "Induction")

    AdvicesConsumption.add_new_advice("Consommation Bouilloire", "On utilise la m??me quantit?? d?????nergie pour chauffer de l???eau avec une bouilloire ??lectrique, un micro-onde, une gazi??re, une plaque ?? induction ou une taque ??lectrique. ", "Bouilloire")
    AdvicesConsumption.add_new_advice("Consommation Bouilloire", "Chauffer l'??quivalent d'une tasse de th?? avec des appareils de m??me puissance donne les r??sultats suivants", "Bouilloire")
    AdvicesConsumption.add_new_advice("Consommation Bouilloire", "Bouilloire ??lectrique: 50 sec pour une consommation de 0.02 kWh", "Bouilloire")
    AdvicesConsumption.add_new_advice("Consommation Bouilloire", "Micro-ondes: 2 minutes pour une consommation de 0.04 kWh", "Micro-ondes")
    AdvicesConsumption.add_new_advice("Consommation Bouilloire", "Gazini??re ou plaque ??lectrique(sans induction): plus de 3 minutes pour une consommation de 0.07 kWh", "Gazini??re")
    AdvicesConsumption.add_new_advice("Consommation Bouilloire", "Les diff??rences sont encore plus grandes si l???on chauffe 1 litre d???eau.", "Bouilloire")
    AdvicesConsumption.add_new_advice("Consommation Bouilloire", "Si on convertit ces consommations en euro, vu qu???1 kWh de gaz co??te moins cher qu???1 kWh d?????lectricit??, le gaz est la source d?????nergie la plus ??conomique.", "Bouilloire")

    MeasureConsumption.query.delete()