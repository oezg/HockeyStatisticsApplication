import json

class HockeyPlayer:
    def __init__(self, player_stats: dict) -> None:
        self.__stats = player_stats
    
    @property
    def name(self) -> str:
        return self.__stats['name']

    @property
    def team(self) -> str:
        return self.__stats['team']

    @property
    def nationality(self) -> str:
        return self.__stats['nationality']

    @property
    def goals(self) -> int:
        return self.__stats['goals']

    @property
    def assists(self) -> int:
        return self.__stats['assists']

    @property
    def points(self) -> int:
        return self.goals + self.assists

    @property
    def games(self) -> int:
        return self.__stats['games']

    def __str__(self) -> str:
        return f"{self.name:20} {self.team} {self.goals:3} + {self.assists:2} = {self.points:3}"

class PlayerStatistics:
    def __init__(self) -> None:
        self.__players = {}

    @property
    def players(self) -> dict:
        return self.__players

    def search_for_player(self, name: str) -> HockeyPlayer:
        if name in self.players:
            return self.players[name]

    def add_player(self, player_stats: dict) -> None:
        player = HockeyPlayer(player_stats)
        self.players[player.name] = player

    def teams(self) -> list:
        return sorted(set(player.team for player in self.players.values()))

    def countries(self) -> list:
        return sorted(set(player.nationality for player in self.players.values()))

    def players_in_team(self, team: str) -> list:
        return sorted(filter(lambda x: x.team == team, self.players.values()), key=lambda x: x.points, reverse=True)

    def players_from_country(self, country: str) -> list:
        return sorted(filter(lambda x: x.nationality == country, self.players.values()), key=lambda x: x.points, reverse=True)

    def players_with_most_points(self, number: int) -> list:
        return sorted(self.players.values(), key=lambda x: (x.points, x.goals), reverse=True)[:number]
    
    def players_with_most_goals(self, number: int) -> list:
        return sorted(self.players.values(), key=lambda x: (x.goals, -x.games), reverse=True)[:number]

class HockeyStatisticsApplication:
    def __init__(self) -> None:
        self.__stats = PlayerStatistics()
    
    @property
    def stats(self) -> PlayerStatistics:
        return self.__stats

    def help(self) -> None:
        print("commands:")
        print("0 quit")
        print("1 search for player")
        print("2 teams")
        print("3 countries")
        print("4 players in team")
        print("5 players from country")
        print("6 most points")
        print("7 most goals")

    def read_data(self) -> None:
        filename = input("file name: ")
        with open(filename) as file:
            season = json.load(file)
            player_count = 0
            for player_stats in season:
                self.stats.add_player(player_stats)
                player_count += 1
            print(f"read the data of {player_count} players")

    def search_for_player(self) -> None:
        """Search by name for a single player's stats and print it
        """
        name = input("name: ")
        player = self.stats.search_for_player(name)
        print(player)

    def print_teams(self) -> None:
        """Retrieve the list of all the abbreviations for team names in alphabetical order and print it
        """
        teams = self.stats.teams()
        for team in teams:
            print(team)

    def print_countries(self) -> None:
        """Retrieve the list of all the abbreviations for countries in alphabetical order
        Print the list
        """
        countries = self.stats.countries()
        for country in countries:
            print(country)
    
    def players_in_team(self) -> None:
        """Retrieve the list of players in a specific team 
        Print them in the order of points scored, from highest to lowest 
        Points equals goals + assists
        """
        team = input("team: ")
        players = self.stats.players_in_team(team)
        print()
        for player in players:
            print(player)

    def players_from_country(self) -> None:
        """Retrieve the list of players from a specific country
        Print them in the order of points scored, from highest to lowest
        """
        country = input("country: ")
        players = self.stats.players_from_country(country)
        print()
        for player in players:
            print(player)

    def most_points(self) -> None:
        """Retrieve the list of input number of players who've scored the most points and print them
        If two players have the same score, whoever has scored the higher number of goals comes first
        """
        number = int(input("how many: "))
        players = self.stats.players_with_most_points(number)
        print()
        for player in players:
            print(player)

    def most_goals(self) -> None:
        """Retrieve the list of input number of players who've scored the most goals and print them
        If two players have the same number of goals, whoever has played the lower number of games comes first
        """
        number = int(input("how many: "))
        players = self.stats.players_with_most_goals(number)
        print()
        for player in players:
            print(player)


    def execute(self) -> None:
        self.read_data()
        print()
        self.help()
        while True:
            print()
            command = input("command: ")
            if command == "0":
                break
            elif command == "1":
                self.search_for_player()
            elif command == "2":
                self.print_teams()
            elif command == "3":
                self.print_countries()
            elif command == "4":
                self.players_in_team()
            elif command == "5":
                self.players_from_country()
            elif command == "6":
                self.most_points()
            elif command == "7":
                self.most_goals()
            else:
                self.help()
            

application = HockeyStatisticsApplication()
application.execute()