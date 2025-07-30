Код для второго задания: 

```java
package server;

import utils.Constants;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Server {
    private int port;
    ArrayList<ClientAPI> clients = new ArrayList<>();
    
    public Server(int port) {
        this.port = port;
    }
    
    public void start() throws IOException {
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Сервер запущен. Порт: " + port);
            while (true) {
                Socket clientSocket = serverSocket.accept();
                ClientAPI client = new ClientAPI(this, clientSocket);
                clients.add(client);
                client.start();
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
    
    public void broadcast(String message) {
        for (ClientAPI client : clients)
            client.sendMessage(message);
    }
    
    public static void main(String[] args) {
        try {
            new Server(Constants.port).start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```