from rest_framework import viewsets

from cinema.models import Movie, Genre, Actor, MovieSession, CinemaHall
from cinema.serializers import (
    GenreSerializer,
    ActorSerializer,
    MovieListSerializer,
    MovieRetrieveSerializer,
    MovieSerializer,
    MovieSessionSerializer,
    MovieSessionRetrieveSerializer,
    MovieSessionListSerializer,
    CinemaHallSerializer,
    ActorDetailSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActorDetailSerializer
        return ActorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieRetrieveSerializer
        return MovieSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("genres", "actors")
        return queryset


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all().select_related(
        "movie",
        "cinema_hall"
    )

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionListSerializer
        elif self.action == "retrieve":
            return MovieSessionRetrieveSerializer
        return MovieSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related("movie", "cinema_hall")
        return queryset


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
