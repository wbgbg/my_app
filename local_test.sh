echo 注册用户root
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"root","password":"root"}' http://localhost:8080/api/users
echo 请求token
curl -u root:root -i -X GET http://localhost:8080/api/token
echo 关注商品1271499
curl -u root:root -i -X POST -H "Content-Type:application/json" -d '{"hkd":"1217499"}' http://localhost:8080/api/favorite/add
echo 查询1217499价格
curl -u root:root -i -X GET http://localhost:8080/api/fetch/1217499
echo 请求用户收藏的商品
curl -u root:root -i -X GET http://localhost:8080/api/favorite
#echo 删除商品1271499
#curl -u root:root -i -X POST -H "Content-Type:application/json" -d '{"hkd":"1217499"}' http://localhost:8080/api/favorite/del
#echo 请求用户收藏的商品
#curl -u root:root -i -X GET http://localhost:8080/api/favorite
#echo 删除数据库
#rm /home/yugi/db.sqlite


