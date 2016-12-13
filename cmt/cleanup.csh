# echo "cleanup MLTree MLTree-00-00-00 in /share/home/jolsson/workarea/MLTreeAthenaAnalysis"

if ( $?CMTROOT == 0 ) then
  setenv CMTROOT /cvmfs/atlas.cern.ch/repo/sw/software/x86_64-slc6-gcc49-opt/20.7.7/CMT/v1r25p20160527
endif
source ${CMTROOT}/mgr/setup.csh
set cmtMLTreetempfile=`${CMTROOT}/${CMTBIN}/cmt.exe -quiet build temporary_name`
if $status != 0 then
  set cmtMLTreetempfile=/tmp/cmt.$$
endif
${CMTROOT}/${CMTBIN}/cmt.exe cleanup -csh -pack=MLTree -version=MLTree-00-00-00 -path=/share/home/jolsson/workarea/MLTreeAthenaAnalysis  $* >${cmtMLTreetempfile}
if ( $status != 0 ) then
  echo "${CMTROOT}/${CMTBIN}/cmt.exe cleanup -csh -pack=MLTree -version=MLTree-00-00-00 -path=/share/home/jolsson/workarea/MLTreeAthenaAnalysis  $* >${cmtMLTreetempfile}"
  set cmtcleanupstatus=2
  /bin/rm -f ${cmtMLTreetempfile}
  unset cmtMLTreetempfile
  exit $cmtcleanupstatus
endif
set cmtcleanupstatus=0
source ${cmtMLTreetempfile}
if ( $status != 0 ) then
  set cmtcleanupstatus=2
endif
/bin/rm -f ${cmtMLTreetempfile}
unset cmtMLTreetempfile
exit $cmtcleanupstatus

