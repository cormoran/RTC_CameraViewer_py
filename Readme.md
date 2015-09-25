#CameraViewer_py

pythonで書いたCameraImageを表示するRTC

#Development Environment
- Mac OSX Yosemite
- Python 2.7
- OpenCV 2.4
- numpy

Windows8.1でも動作確認済み

#Problem
- 遅い（おそらくCameraImageからnumpy arrayに変換している所がネック）
- 素直にc++版使うのが良さそう
