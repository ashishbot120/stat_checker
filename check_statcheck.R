.libPaths('C:/ashish/stat-checker/Rlib')
library(statcheck)
cat('Package version:', as.character(packageVersion('statcheck')), '\n')
cat('checkPDFdir present:', ('checkPDFdir' %in% ls('package:statcheck')), '\n')
