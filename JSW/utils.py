import rospy
import tf2_ros

def get_transform_matrix(target_frame, source_frame, time=None):
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)

    if time is None:
        time = rospy.Time(0)
    try:
        trans = tf_buffer.lookup_transform(target_frame, source_frame, time, rospy.Duration(1.0))
        t = trans.transform.translation
        q = trans.transform.rotation
        import tf.transformations as tft
        trans_mat = tft.quaternion_matrix([q.x, q.y, q.z, q.w])
        trans_mat[0, 3] = t.x
        trans_mat[1, 3] = t.y
        trans_mat[2, 3] = t.z
        return trans_mat
    except Exception as e:
        rospy.logwarn(f"TF lookup failed: {e}")
        return None