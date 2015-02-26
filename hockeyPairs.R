

#' xml data

#+ vWinnipeg
library('XML')

x=readHTMLTable('http://www.nhl.com/scores/htmlreports/20142015/TH020224.HTM',as.is=TRUE)

library('RCurl')
webpage <- getURL('http://www.nhl.com/scores/htmlreports/20142015/TH020224.HTM')

webpage <- readLines(tc <- textConnection(webpage)); close(tc)
pagetree <- htmlTreeParse(webpage, error=function(...){},useInternalNodes=TRUE)


x <- xpathSApply(pagetree, "//*/table/tr/td", xmlValue)

x = gsub(" / [[:digit:]]+:[[:digit:]]+$","", x)
x = gsub("Elapsed / Game$","", x)
x = gsub("of Shift$","", x)
players = grep("^[[:digit:]]+ ", x)
per = grep("^Per$", x)

dateRow=grep("[[:alpha:]]+ [[:digit:]]+, 201[[:digit:]]$",x)
xdate = x[dateRow]
xdate = gsub("^[[:alpha:]]+, ", "", xdate)

res = NULL
twentyminutes = 20*60

for(Dplayer in 1:length(players)) {

h1 = x[seq(players[Dplayer]+1, 
        players[Dplayer]+6)]
p1 = matrix(x[seq(
            players[Dplayer]+1+6, 
            sort(per[per>players[Dplayer]])[2]-3)
], ncol=6,byrow=TRUE)
colnames(p1) = h1
cplayer = x[players[Dplayer]]
p1 = cbind(
    player=gsub("^[[:digit:]]+ ", "", cplayer), 
    number = strsplit(cplayer, " ")[[1]][1],
    p1)

p1 = as.data.frame(p1)

p1$number = as.numeric(p1$number)
p1$Per = as.numeric(p1$Per)
p1$Start = strptime(paste(xdate, p1$Start), 
    "%B %d, %Y %M:%S") + twentyminutes*(p1$Per-1)
p1$End = strptime(paste(xdate, p1$End),
    "%B %d, %Y %M:%S") + twentyminutes*(p1$Per-1)

res = rbind(res, p1)

}

res[1:4,1:6]
#'
#' 
#' convert to intervals

#+ iranges
library('intervals')    
   
res$intervals = Intervals(cbind(
        as.integer(res$Start),
        as.integer(res$End)
        ),
        closed=c(FALSE,TRUE))
#'


#+ overlap
Splayers = unique(as.character(res$player))
allPairs = expand.grid(Splayers,Splayers)
theLower = 
    matrix(1:nrow(allPairs),ncol=length(Splayers))
theLower = theLower[lower.tri(theLower,diag=FALSE)]
allPairs = allPairs[theLower,]

pairsIntervals = mapply(
  function(p1, p2, data){
    interval_intersection(
        data[data$player==p1,]$intervals,
        data[data$player==p2,]$intervals
        )
  },
p1=as.character(allPairs[,1]),
p2=as.character(allPairs[,2]),
MoreArgs=list(data=res)
)
names(pairsIntervals) = paste(allPairs[,1], allPairs[,2],sep=' / ')
#'



#+ plotRangesFunction, echo=FALSE    
plotRanges <- function(data, pairs,
    p1='subban',p2='markov',
        ...) 
    {
      p1 = grep(p1, data$player, ignore.case=TRUE,value=TRUE)[1]
      p2 = grep(p2, data$player, ignore.case=TRUE,value=TRUE)[1]
      
      thePair = intersect(
          grep(p1, names(pairs), value=TRUE),
          grep(p2, names(pairs), value=TRUE)
          )
      
      xList = list(
          data[data$player==p1,]$intervals, 
          data[data$player==p2,]$intervals, 
          pairs[[thePair]]
          )
       names(xList) = c(p1, p2, 
           'Both')    
     


      forX = as.POSIXct(
          as.integer(unlist(xList)),
            origin= '1970-01-01 00:00.00 UTC'
        )
        par(oma=c(0,6,0,0))
        plot(range(forX), 
            c(0,length(xList)+1),
            yaxt='n', ylab='', xlab='time',
            main=format(forX[1],'%d %B %Y'),
            type='n',
            ...
            )
        axis(2, at=1:length(xList),
            names(xList)    ,las=2
            )
         
        for(Dplayer in 1:length(xList)){
          for(Dshift in 1:nrow(xList[[Dplayer]]))
            lines(xList[[Dplayer]][Dshift,],
                rep(Dplayer,2),
                type='o',
                pch=c(16,1),cex=0.6)
        }
    }
#'
toi = unlist(lapply(pairsIntervals, function(qq) sum(size(qq))))
toi[1:10]

#' plot the data

#+ plotShifts, fig.cap='shifts'

plotRanges(res,pairsIntervals,'eller','markov')
#'



  