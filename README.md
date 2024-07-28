### Run
```docker-compose up```

### Stop 
```cntrl + c ```

### Rebuild 
stop using
```docker-compose down ``` 
and run
```docker-compose up --build```

### Remove Redis data directory for a clean redis db
#### Make sure to stop the instance before running this

```docker volume rm  InsertToRedisTest_redis_data```


### Monitor the docker services data and usage 
```docker stats```
