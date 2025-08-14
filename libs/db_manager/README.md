Batteries Curl command:
POST:
```bash
curl -X POST http://192.168.8.109:5000/batteries/ -H "Content-Type: application/json" -d '{"step_index":1,"voltage1":12.5,"voltage2":12.4,"voltage3":12.3,"current1":1.2,"current2":1.1,"current3":1.3,"temperature1":25.4,"temperature2":26.1,"temperature3":25.8}'
```
GET:
```bash
curl -X GET http://192.168.8.109:5000/batteries/
```
GET Latest:
```bash
curl -X GET http://192.168.8.109:5000/batteries/latest
```
### **External Pressure**

**POST**

```bash
curl -X POST http://192.168.8.109:5000/external_pressure -H "Content-Type: application/json" -d '{"step_index":1,"pressure":101.3}'
```

**GET (all pressures)**

```bash
curl -X GET http://192.168.8.109:5000/external_pressure
```

**GET (latest pressure)**

```bash
curl -X GET http://192.168.8.109:5000/external_pressure/latest
```

---

### **External Depth**

**POST**

```bash
curl -X POST http://192.168.8.109:5000/external_depth -H "Content-Type: application/json" -d '{"step_index":1,"depth":12.4}'
```

**GET (all depths)**

```bash
curl -X GET http://192.168.8.109:5000/external_depth
```

**GET (latest depth)**

```bash
curl -X GET http://192.168.8.109:5000/external_depth/latest
```

### **POST (add IMU data)**

```bash
curl -X POST http://192.168.8.109:5000/imu/ -H "Content-Type: application/json" -d '{"step_index":1,"accel_x":0.12,"accel_y":0.05,"accel_z":9.81,"gyro_x":0.01,"gyro_y":0.02,"gyro_z":0.03}'
```

### **GET (all IMU data)**

```bash
curl -X GET http://192.168.8.109:5000/imu/
```

### **GET (latest IMU entry)**

```bash
curl -X GET http://192.168.8.109:5000/imu/latest
```

### **POST (add input)**

```bash
curl -X POST http://192.168.8.109:5000/inputs/ -H "Content-Type: application/json" -d '{"step_index":1,"direction":"forward","force":0.75,"s1":0.1,"s2":0.2,"s3":0.3,"arm":true}'
```

### **GET (all inputs)**

```bash
curl -X GET http://192.168.8.109:5000/inputs/
```

### **GET (latest input)**

```bash
curl -X GET http://192.168.8.109:5000/inputs/latest
```

### Internal Temperature

```bash
curl -X POST http://192.168.8.109:5000/internal_temperature -H "Content-Type: application/json" -d '{"step_index":1,"temperature":25.6}'
```

```bash
curl -X GET http://192.168.8.109:5000/internal_temperature
```

```bash
curl -X GET http://192.168.8.109:5000/internal_temperature/latest
```

### Internal Humidity

```bash
curl -X POST http://192.168.8.109:5000/internal_humidity -H "Content-Type: application/json" -d '{"step_index":1,"humidity":45.2}'
```

```bash
curl -X GET http://192.168.8.109:5000/internal_humidity
```

```bash
curl -X GET http://192.168.8.109:5000/internal_humidity/latest
```

### Internal Pressure

```bash
curl -X POST http://192.168.8.109:5000/internal_pressure -H "Content-Type: application/json" -d '{"step_index":1,"pressure":101.3}'
```

```bash
curl -X GET http://192.168.8.109:5000/internal_pressure
```

```bash
curl -X GET http://192.168.8.109:5000/internal_pressure/latest
```

### POST (add output)

```bash
curl -X POST http://192.168.8.109:5000/outputs/ -H "Content-Type: application/json" -d '{"step_index":1,"direction":"forward","force":0.75,"M1":0.1,"M2":0.2,"M3":0.3,"M4":0.4,"M5":0.5,"M6":0.6,"M7":0.7,"M8":0.8,"S1":0.11,"S2":0.22,"S3":0.33,"arm":true}'
```

### GET (all outputs)

```bash
curl -X GET http://192.168.8.109:5000/outputs/
```

### GET (latest output)

```bash
curl -X GET http://192.168.8.109:5000/outputs/latest
```

### POST (add sonar reading)

```bash
curl -X POST http://192.168.8.109:5000/sonar/ -H "Content-Type: application/json" -d '{"step_index":1,"distance":3.42,"angle":57.0}'
```

### GET (all sonar readings)

```bash
curl -X GET http://192.168.8.109:5000/sonar/
```

### GET (latest sonar reading)

```bash
curl -X GET http://192.168.8.109:5000/sonar/latest
```
