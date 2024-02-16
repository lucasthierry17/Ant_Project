class Ant:
    def __init__():
        pass

    def look():
        """
        Hier wird das Aussehen der Ameisen definiert.
        """
        pass

    def movement():
        """
        Hier wird die Bewegung der Ameise festgelegt. Sie kann in allen Richtungen unendlich weit laufen
        Die Bewegung geschieht zufällig und hat vor dem Entdecken der Nahrung keine Regeln.
        Bei jeder Bewgung werden Pheromone freigesetzt, die später näher definiert werden.
        Das Nest wird zufällig auf der Karte in map.py gesetzt. Wichtig ist, dass die Ameise ihren Startpunkt kennt und dass jener in einer Variabel gespeichert wird.
        Diese Info wird nämlich später in der memory-Funktion wichtig.
        """
        pass

    def memory():
        """
        In der Erinnerung werden die wichtigsten Datenpunkte auf der Karte gespeichert:
        Die Futterquellen, Das Nest, Hindernisse etc.
        Diese werden von der Ameise entweder angepeilt oder gemieden.
        Die Erinnerung der Ameise, wird natürlich immer wieder aktualisiert, sofern sie eine neue Futterquelle entdeckt oder die bereits bekannte
        Futterquelle verbraucht ist.
        """
        pass

    def perception():
        """
        Hier wird die Wahrnehmung der Ameise festegelegt. Die Ameise kann in einem gewissen Umkreis ihre Umgebeung wahrnehmen und
        mögliche Futterquellen oder Futterkanäle identifizieren.
        Diese könnten in der memory der Ameise gespeichert werden.
        """
        pass

    def pheromone():
        """
        Die Pheromone der Ameisen legen ihren "Status" fest. Die Pheromone werden auf ihrem Pfad entlang ausgelassen:
        Status: Nahrung gefunden.
        Status: Keine Nahrung und auf der Suche nach Nahrung.

        """
        pass

    def approach():
        """
        Für Hindernisse um sie zu identifizieren???
        """
        pass

    def gohome():
        """
        Ist sehr trivial. Wie der Name schon sagt sorgt diese Funktion dafür, dass die Ameise wieder zurück in ihr Nest gelangt.
        Am besten ist der kürzeste Weg dahin.
        """
        pass

    def die():
        """
        Ist sehr trivial. Sobald die Ameise ein Hindernis nicht erkennt stirbt sie. (Mögliche Hindernisse:
        Loch, Pfütze,....)
        """
        pass

    def take_food():
        """
        Sobald die Ameise die Nahrungsquelle gefunden hat soll die Ameise, die Nahrung aufnehmen.
        Damit ändert sich der pheromonen Status und die Ameise macht sich auf den Weg ins Nest.
        """
        pass

    def follow_pheromone():
        """
        follow_pheromone macht genau das was der Name sagt. Soabld die Ameise die Pheromonen der anderen Ameisen wahrnimmt
        und diese auf den Status "Nahrung gefunden gesetzt sind", dann beginnt die Ameise dieser Spur zu folgen bis sie eine Nahrungsquelle gefunden hat
        um ihren Pheromonen Status auch zu ändern.
        """
        pass
