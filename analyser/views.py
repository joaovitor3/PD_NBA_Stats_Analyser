from django.shortcuts import render

from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django_tables2.utils import A

import django_tables2 as tables
from django_tables2.config import RequestConfig


from analyser.models import Stats
from analyser.utils import get_player_table_data
from analyser.filters import StatsFilter
from analyser.algorithms import longest_subsequence


class PlayerTable(tables.Table):
    player_name = tables.Column()
    player_team = tables.Column()
    game = tables.Column(order_by=("game_date"))
    game_date = tables.Column(visible=False)
    points = tables.Column()
    rebounds = tables.Column()
    assists = tables.Column()
    blocks = tables.Column()

class SubSequenceTable(tables.Table):
    player_name = tables.Column()
    subsequence = tables.Column()


def player_stats(request, pk):
    player_table_data, subsequence_data = get_player_table_data(pk)
    table = PlayerTable(data=player_table_data)

    RequestConfig(request, paginate={"per_page":10}).configure(table)

    current_page_data = table.paginated_rows.data
    analysis_criteria = {
        "points": {
            "selected": False
        },
        "rebounds": {
            "selected": False
        },
        "assists": {
            "selected": False
        },
        "blocks": {
            "selected": False
        },
    }
    criteria = request.GET.get("criteria", "points")
    analysis_criteria[criteria]["selected"] = True

    players = {}

    for i, data in enumerate(current_page_data):
        player_team = data["player_team"]
        player_name = data["player_name"]

        if player_team in players:
            players[player_team]["length"] += 1
        else:
            players[player_team] = {
                "start": i,
                "length": 1
            }

        if player_name in players:
            players[player_name]["length"] += 1
        else:
            players[player_name] = {
                "start": i,
                "length": 1
            }

    context = {
        "table": table,
        'row_span_data': [
            table.columns["player_team"],
            table.columns["player_name"]
        ],
        "players": players,
        "analysis_criteria": analysis_criteria,
        "criteria": criteria,
        "subsequence": longest_subsequence(subsequence_data[criteria]),
        "player_name": subsequence_data["player_name"],
        "player_id": pk,
    }

    return render(request, 'player.html', context)


def home(request):
    return render(request, 'home.html')

class StatsTable(tables.Table):
    games = tables.ManyToManyColumn(verbose_name="Game")
    player = tables.LinkColumn("player_stats", args=[A("player.id")])
    player_team = tables.Column(accessor="player.team", verbose_name="Player Team")

    class Meta:
        model = Stats
        fields = (
            "player", "player_team", "games", "points", "rebounds", "assists", "blocks"
        )

class StatsListView(SingleTableMixin, FilterView):
    model = Stats
    paginate_by = 20
    table_class = StatsTable
    template_name = 'stats.html'
    pagination_class = tables.paginators.LazyPaginator


    filterset_class = StatsFilter

    def get_page_data(self, table, page_number=1):
        current_page = table.paginate(
            page=self.request.GET.get("page", page_number),
            per_page=self.paginate_by
        )
        current_page_data = current_page.paginated_rows.data
        return current_page_data


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        stats = Stats.objects.all()

        stats_filter = StatsFilter(self.request.GET, queryset=stats)
        has_filter = any(
            field in self.request.GET for field in set(stats_filter.get_fields())
        )

        table = self.get_table(**self.get_table_kwargs(), orderable=False)

        current_page_data = self.get_page_data(table)
        teams = {}
        for i, data in enumerate(current_page_data):
            player_team = data.player.team.name
            game = data.games.all().first()

            if data.player.team.name in teams:
                teams[player_team]["length"] += 1
            else:
                teams[player_team] = {
                    "start": i,
                    "length": 1
                }
            if game.slug in teams:
                teams[game.slug]["length"] += 1
            else:
                teams[game.slug] = {
                    "start": i,
                    "length": 1
                }

        context = {
            'stats_filter':stats_filter,
            'has_filter': has_filter,
            'row_span_data': [
                table.columns["player_team"],
                table.columns["games"]
            ],
            'teams': teams,
            self.get_context_table_name(table): table
        }
        return context
