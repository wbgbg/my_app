echo 注册用户root
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"root","password":"root"}' http://localhost:5000/api/users
echo 请求token
curl -u root:root -i -X GET http://localhost:5000/api/token
echo 关注商品1271499
curl -u root:root -i -X POST -H "Content-Type:application/json" -d '{"hkd":"1217499"}' http://localhost:5000/api/favorite/add
echo 请求用户收藏的商品
curl -u root:root -i -X GET http://localhost:5000/api/favorite
echo 删除商品1271499
curl -u root:root -i -X POST -H "Content-Type:application/json" -d '{"hkd":"1217499"}' http://localhost:5000/api/favorite/del
echo 请求用户收藏的商品
curl -u root:root -i -X GET http://localhost:5000/api/favorite
echo 删除数据库
rm /home/yugi/db.sqlite


