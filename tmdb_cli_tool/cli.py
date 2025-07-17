import click
from .tmdb import call
from requests.exceptions import RequestException, HTTPError

@click.group()
def cli():
    """TMDB CLI Tool"""

@cli.command()
@click.argument("query")
@click.option("--page", default=1, help = "Page number")
def search_movie(query, page):
    """Search movies by title"""
    try:
        data = call("/search/movie", {"query": query, "page": page})
    except HTTPError as e: #Invalid querys don't count as HTTPErrors
        raise click.ClickException(f"TMDB API error: {e.response.status_code} {e.response.reason}")
    except RequestException as e:
        raise click.ClickException(f"Network error: {e}")
    
    results = data.get("results", []) #results is either list of movies of empty list
    if not results: #raises exception if empty list
        raise click.ClickException(f"No movies found matching '{query}'.")

    for m in results: #Display results
        year = m.get("release_date", "")[:4]
        click.echo(f"{m['id']:6}  {m['title']} ({year})")


@cli.command()
@click.argument("movie_id", type = int)
def info_movie(movie_id):
    """Get movie details by ID"""
    try:
        m = call(f"/movie/{movie_id}")
    except HTTPError as e:
        raise click.ClickException(f"TMDB API error: {e.response.status_code} {e.response.reason}")
    except RequestException as e:
        raise click.ClickException(f"Network error: {e}")
    
    click.echo(f"Title:       {m.get('title','N/A')}")
    click.echo(f"Release:     {m.get('release_date','N/A')}")
    click.echo(f"Rating:      {m.get('vote_average','N/A')} / 10")
    click.echo(f"Vote count:  {m.get('vote_count',0)}")
    click.echo(f"Overview:    {m.get('overview','')}")


@cli.command("popular-movies")
@click.option("--page", default=1, show_default=True,
              help="Page of results to fetch")
@click.option("--language", default=None,
              help="Language code (e.g. en-US)")
@click.option("--region", default=None,
              help="Specify a country code for regional popularity")
def popular_movies(page, language, region):
    """
    List the current most popular movies.
    """
    params = {"page": page}
    if language:
        params["language"] = language
    if region:
        params["region"] = region

    data = call("/movie/popular", params)
    results = data.get("results", [])
    if not results:
        raise click.ClickException(f"No upcoming movies found (page {page}).")

    for m in results:
        year = m.get("release_date", "")[:4]
        rating = round(m.get("vote_average", ""), 1)
        click.echo(f"{m['id']:6}  {m['title']} ({year}) ({rating} / 10)")


@cli.command("upcoming-movies")
@click.option("--page", default=1, show_default=True, help="Page of results to fetch")
@click.option("--language", default=None, help="Language code (e.g. en-US)")
@click.option("--region", default=None, help="Specify a country code for regional release dates")
def upcoming_movies(page, language, region):
    """
    List the upcoming movies.
    """
    try:
        params = {"page": page}
        if language:
            params["language"] = language
        if region:
            params["region"] = region

        data = call("/movie/upcoming", params)
    except HTTPError as e:
        raise click.ClickException(
            f"TMDB API error {e.response.status_code}: {e.response.reason}"
        )
    except RequestException as e:
        raise click.ClickException(f"Network error: {e}")

    results = data.get("results", [])
    if not results:
        raise click.ClickException(f"No upcoming movies found (page {page}).")

    for m in results:
        year = m.get("release_date", "")[:4]
        click.echo(f"{m['id']:6}  {m['title']} ({year})")


if __name__ == "__main__":
    cli()