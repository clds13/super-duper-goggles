## Frame Logging

### Testing

Used [this](https://www.grun1.com/utils/timeDiff.cfm) site to calculate time differences from CSV output.

#### Test 1 Setup

**February 22, 2024**

| Parameter  | Value  |
| ---------- | ------ |
| FPS        | 30     |
| Resolution | High   |
| Projector  | Off    |

#### Test 1 Results

| Recording Duration | Metadata Duration | Difference |
| ------------------ | ----------------- | ---------- |
| 10 sec             | 11.93 sec         | 1.93 sec   |
| 60 sec             | 69.54 sec         | 9.54 sec   |

---

#### Test 2 Setup

**February 22, 2024**

| Parameter  | Value  |
| ---------- | ------ |
| FPS        | 20     |
| Resolution | High   |
| Projector  | Off    |

#### Test 2 Results

| Recording Duration | Metadata Duration | Difference |
| ------------------ | ----------------- | ---------- |
| 10 sec             | 9.95 sec          | -0.05 sec  |
| 60 sec             | 59.95 sec         | -0.05 sec  |
| 120 sec            | 119.96 sec        | -0.04 sec  |
| 300 sec            | 299.94 sec        | -0.06 sec  |


---

#### Test 3 Setup

**February 22, 2024**

| Parameter  | Value  |
| ---------- | ------ |
| FPS        | 20     |
| Resolution | High   |
| Projector  | On     |

#### Test 3 Results

| Recording Duration | Metadata Duration | Difference |
| ------------------ | ----------------- | ---------- |
| 900 sec            | 900.09 sec        | 0.09 sec   |

---

#### Test 4 Setup

In this test, the call to log each frame (`await logger.log_frame(frame_count, timestamp)`) has been moved to *before* the call to `video_writer.write(high_res_frame)` which adds a new frame to the video. Tests 1 - 3 called the logging *after* the frame was written.

**February 23, 2024**

| Parameter  | Value  |
| ---------- | ------ |
| FPS        | 20     |
| Resolution | High   |
| Projector  | On     |

#### Test 4 Results

| Recording Duration | Metadata Duration | Difference |
| ------------------ | ----------------- | ---------- |
| 60 sec             | 59.95 sec         | -0.05 sec  |
| 120 sec            | 119.95 sec        | -0.05 sec  |
| 300 sec            | 299.96 sec        | -0.04 sec  |
| 600 sec            | 599.97 sec        | -0.03 sec  |
