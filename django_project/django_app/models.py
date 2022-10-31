from tempfile import NamedTemporaryFile
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from django.core.files import File
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/avatars/', verbose_name='Avatar', blank=True)
    image_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if self.image_url and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            try:
                img_temp.write(urlopen(self.image_url).read())
                img_temp.flush()
                self.image.save(
                    f"image_{self.image_url[self.image_url.rfind('/')+1:]}", File(img_temp)
                )
            except HTTPError as e:
                print(e)
            except URLError as e:
                print(e)
            except BaseException as e:
                print(e)
        super(Profile, self).save(*args, **kwargs)
