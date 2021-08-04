# Rescue-Warning

Bài toán cảnh báo cứu hộ

Hướng dẫn cài đặt thư viện:

1. git clone https://www.github.com/ildoonet/tf-pose-estimation

2. cd tf-pose-estimation

3. pip install -r requirements.txt

4. (Windows 10) setting swig https://simpletutorials.com/c/2135/Installing+SWIG+on+Windows

5. cd tf_pose/pafprocess

6. swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace

7. pip install slidingwindow

8. pip install cython

9. install pycocotools https://github.com/matterport/Mask_RCNN/issues/6#issuecomment-341503509

10. download model http://www.mediafire.com/file/qlzzr20mpocnpa3/graph_opt.pb và copy vào thư mục models\graph\cmu

    

Hướng phát triển sản phẩm:

Phase 1:

- [x] Đếm số lượng người
- [x] Phát hiện hành động dơ tay và cảnh báo (1 đối tượng)
- [x] Phát hiện người (bbox) khi có tín hiệu cảnh báo (1 đối tượng)
- [x] Xử lý đa luồng: luồng 1 phát hiện dơ tay, luồng 2 phát hiện người dơ tay (1 đối tượng)

Phase 2:

- [x] Phát hiện hành động dơ tay và cảnh báo (nhiều đối tượng)

- [x] Phát hiện người (bbox) khi có tín hiệu cảnh báo (nhiều đối tượng)

- [x] Xử lý đa luồng: luồng 1 phát hiện dơ tay, luồng 2 phát hiện người dơ tay (nhiều đối tượng)

- [x] Xử lý tín hiệu cảnh báo cho mỗi người

- [x] Áp dụng sort tracking để theo dõi và làm giảm việc xử lý phải detect liên tục

  

Phase 3:



- [ ] Deploy ứng dụng

- [ ] Deploy service

  

Phase 4:

- [ ] Xử lý realtime

