import httpx


class MetricsService:

    url = 'https://api.github.com/repos/ledxdeliveryflopp/WarThunderDiscordRPC/releases' # noqa

    def get_releases_data(self) -> list[dict]:
        response = httpx.get(self.url)
        releases = response.json()
        return releases

    def get_download_counts(self) -> None:
        releases = self.get_releases_data()
        for release in releases:
            release_tag = release['tag_name']
            download_count = release['assets'][0]['download_count']
            print('-' * 10)
            print(f'Release -> {release_tag}')
            print(f'Download Count -> {download_count}')
            print('-' * 10)


if __name__ == '__main__':
    metrics = MetricsService()
    metrics.get_download_counts()