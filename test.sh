echo 注册用户user2
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"user2","password":"heihei"}' http://121.40.220.116:80/api/users
echo 请求token
curl -u user2:heihei -i -X GET http://121.40.220.116:80/api/token
echo 关注商品1219499
curl -u user2:heihei -i -X POST -H "Content-Type: application/json" -d '{"hkd":"1219499"}' http://121.40.220.116:80/api/favorite/add
echo 查询1219499价格
curl -u user2:heihei -i -X GET http://121.40.220.116:80/api/fetch/1219499
echo 请求用户收藏的商品
curl -u user2:heihei -i -X GET http://121.40.220.116:80/api/favorite
echo 删除商品1219499
curl -u user2:heihei -i -X POST -H "Content-Type:application/json" -d '{"hkd":"1219499"}' http://121.40.220.116:80/api/favorite/del
echo 请求用户收藏的商品
curl -u user2:heihei -i -X GET http://121.40.220.116:80/api/favorite


