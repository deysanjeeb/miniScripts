
import pandas as pd
import glob
import os
  
# merging the files
joined_files = os.path.join("*.csv")
  
# A list of all joined files is returned
joined_list = glob.glob(joined_files)
  
# Finally, the files are joined
df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)
print(df)
df.to_csv( "combined_csv.csv", index=True, encoding='utf-8')
