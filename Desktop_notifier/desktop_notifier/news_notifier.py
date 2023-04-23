from plyer import notification 

title = 'Hello world!'

message= 'Read this!'

notification.notify(title= title,
                    message= message,
                    app_icon = None,
                    timeout= 10,
                    toast=False)


