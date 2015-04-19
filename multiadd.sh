echo 关注商品1271499~1272499
for i in {1271499..1272499}
do
	curl -u root:root -i -X POST -H "Content-Type:application/json" -d "{\"hkd\":\"$i\"}" http://121.40.220.116:80/api/favorite/add >>/home/logs
done
echo 查询1217499~1272499价格
for i in {1271499..1272499}
do
	curl -u root:root -i -X GET http://121.40.220.116:80/api/fetch/$i >>/home//logs
done
echo 请求用户收藏的商品
curl -u root:root -i -X GET http://121.40.220.116:80/api/favorite  >>/home//logs
#echo 删除商品1271499
#curl -u root:root -i -X POST -H "Content-Type:application/json" -d '{"hkd":"1217499"}' http://121.40.220.116:80/api/favorite/del
#echo 请求用户收藏的商品
#curl -u root:root -i -X GET http://121.40.220.116:80/api/favorite
#echo 删除数据库
#rm /home/yugi/db.sqlite


