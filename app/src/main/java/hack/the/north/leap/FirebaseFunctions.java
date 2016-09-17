package hack.the.north.leap;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

/**
 * Created by Alex on 2016-09-17.
 */
public class FirebaseFunctions {
    public static void setFist(boolean b) {
        DatabaseReference ref = FirebaseDatabase.getInstance().getReference("").child("fist");
        ref.setValue("hi ethan :)");
    }
}
