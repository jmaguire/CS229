liblinearwrite('TEST.csv', 'MATRIX.LIBLINEAR.TEST');
liblinearwrite('TRAIN.csv', 'MATRIX.LIBLINEAR.TRAIN');

system('windows\train.exe MATRIX.LIBLINEAR.TRAIN');
system('windows\predict.exe MATRIX.LIBLINEAR.TEST MATRIX.LIBLINEAR.TRAIN.model MATRIX.LIBLINEAR.TRAIN.output ');
