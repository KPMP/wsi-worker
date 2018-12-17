import java.util.UUID;

public class Uuid {
  public static void main(String[] args) {
    for(int i = 0; i*2 < args.length; i += 2) {
      UUID uuid = UUID.randomUUID();
      System.out.println(String.format(
          "./manual-link %s %s %s",
	  args[i  ],
          args[i+1],
          uuid.toString()
	)
      );
    }
  }
}
