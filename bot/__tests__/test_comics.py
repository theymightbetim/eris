from bot.comics import NewReleases
import bot.settings as settings
from datetime import date
from requests.exceptions import MissingSchema
import os
import pytest


class TestNewReleases():
    new_release = NewReleases()

    def test_new_releases_class_is_instantiated_properly(self):
        self.new_release = NewReleases()
        assert isinstance(self.new_release.date, date)
        assert self.new_release.date == date.today()
        assert isinstance(self.new_release.url, str)
        assert self.new_release.url == "https://www.previewsworld.com/NewReleases/Export?format=txt&releaseDate={}"\
            .format(self.new_release.date.strftime('%m/%d/%Y'))
        assert isinstance(self.new_release.filename, str)
        assert self.new_release.filename == f"files/new-comics-{self.new_release.date.strftime('%m-%d-%y')}.txt"

    @pytest.fixture()
    def delete_url_setup(self):
        self.new_release.url = 'invalid url'
        yield
        self.new_release = NewReleases()

    def test_get_new_releases_without_url(self, delete_url_setup):
        with pytest.raises(MissingSchema):
            self.new_release.get_new_releases()

    def test_get_new_releases_with_no_filename(self):
        self.new_release = NewReleases()
        self.new_release.filename = ''
        file_created = self.new_release.get_new_releases()
        assert file_created == False

    def test_get_new_releases_downloads_file(self):
        self.new_release = NewReleases()
        filename = self.new_release.get_new_releases()
        file_path = os.path.join(settings.ROOT_DIR, filename)
        assert os.path.exists(file_path) == True
        if os.path.exists(file_path):
            os.remove(file_path)