import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Não foi possível abrir a câmera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível receber o quadro (fim do stream?). Saindo ...")
        break
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
