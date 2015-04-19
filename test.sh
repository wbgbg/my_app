echo 注册用户root
curl -i -X POST -H "Content-Type: application/json" -d '{"username":"root","password":"root"}' http://121.40.220.116:80/api/users
echo 请求token
curl -u root:root -i -X GET http://121.40.220.116:80/api/token
echo 关注商品1271499
curl -u root:root -i -X POST -H "Content-Type: application/json" -d '{"hkd":"1217499"}' http://121.40.220.116:80/api/favorite/add
echo 查询1217499价格
curl -u root:root -i -X GET http://121.40.220.116:80/api/fetch/1217499
echo 请求用户收藏的商品
curl -u root:root -i -X GET http://121.40.220.116:80/api/favorite
#echo 删除商品1271499
#curl -u root:root -i -X POST -H "Content-Type:application/json" -d '{"hkd":"1217499"}' http://121.40.220.116:80/api/favorite/del
#echo 请求用户收藏的商品
#curl -u root:root -i -X GET http://121.40.220.116:80/api/favorite
#echo 删除数据库
#rm /home/yugi/db.sqlite


