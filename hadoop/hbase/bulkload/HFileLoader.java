import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.mapreduce.LoadIncrementalHFiles;

/**
 * Created  on 15-6-9.
 */
public class HFileLoader {
    public static void doBulkLoad(String pathToHFile, String tableName){
        try {
            Configuration configuration = new Configuration();
            HBaseConfiguration.addHbaseResources(configuration);
            LoadIncrementalHFiles loadFfiles = new LoadIncrementalHFiles(configuration);
            HTable hTable = new HTable(configuration, tableName);//ָ������
            loadFfiles.doBulkLoad(new Path(pathToHFile), hTable);//��������
            System.out.println("Bulk Load Completed..");
        } catch(Exception exception) {
            exception.printStackTrace();
        }

    }

}