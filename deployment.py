from mediafire.client import (MediaFireClient, File, Folder)

client = MediaFireClient()
client.login(email='rokgembot@gmail.com',
             password='$X4$f!x_AZ%&f)+')

client.upload_file("city.png", "mf:/update/")
