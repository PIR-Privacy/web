# web
Partie web du projet. Le but est de récupérer les cookies d'une liste de sites identifiés comme public.
Ensuite l'idée est de compter le nombre de cookies présents sur le site en questin, d'identifier les domaines auxquels sont liés les cookies, les temps d'expiration

Une des limites est qu'avec selenium, nous récupérons les cookies de deux manières différentes pour avoir les cookies de sessions et les cookies tiers. De ce fait certains cookies sont en double
