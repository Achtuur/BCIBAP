function [event] = read_ricoh_event(filename, varargin)

% READ_RICOH_EVENT reads event information from continuous,
% epoched or averaged MEG data that has been generated by the Ricoh
% MEG system and software and allows those events to be used in
% combination with FieldTrip.
%
% Use as
%   [event] = read_ricoh_event(filename)
%
% See also READ_RICOH_HEADER, READ_RICOH_DATA

% ensure that the required toolbox is on the path
ft_hastoolbox('ricoh_meg_reader', 1);

event   = [];
handles = definehandles;

% get the options, the default is set below
chanindx    = ft_getopt(varargin, 'chanindx');
threshold   = ft_getopt(varargin, 'threshold');
detectflank = ft_getopt(varargin, 'detectflank');

% read the dataset header
hdr = read_ricoh_header(filename);
ch_info = hdr.orig.channel_info.channel;
type = [ch_info.type];
% determine the trigger channels (if not specified by the user)
if isempty(chanindx)
  chanindx = find(type==handles.TriggerChannel);
end
% As for trial selection, refer to the documentation "Getting started with Ricoh data".
if hdr.orig.acq_type==handles.AcqTypeEvokedAve
  % make an event for the average
  acq_cond_tmp = [];
  acq_cond_tmp = getRHdrAcqCond(filename);
  event(1).type     = 'average';
  event(1).sample   = 1;
  event(1).offset   = -acq_cond_tmp.pretrigger_length;
  event(1).duration =  acq_cond_tmp.frame_length;
  event(1).value    =  acq_cond_tmp.multi_trigger.list.name;
  clear acq_cond_tmp;
elseif hdr.orig.acq_type==handles.AcqTypeContinuousRaw
  %% read the trigger id from all trials and the events annotated by users
  % Events detected through the trigger channels
  event_tmp = [];
  event_tmp = getRHdrEvent(filename);
  if ~isempty(event_tmp)
    for i = 1:length(event_tmp)
      event(end+1).sample = event_tmp(i).sample_no + 1;
      event(end  ).type    =  'triginfo';
      if ~isempty(event_tmp(i).name)
        event(end  ).value    =  event_tmp(i).name;
      elseif isempty(event_tmp(i).name) && ~isempty(event_tmp(i).code)
        event(end  ).value    =  event_tmp(i).code; % 1--16
      else
        event(end  ).value    =  'unknown';
      end
    end
  end
  % Events annotated by users during measurements
  annotation_tmp = [];
  annotation_tmp = getRHdrAnnotation(filename);
  if ~isempty(annotation_tmp)
    for i = 1:length(annotation_tmp)
      event(end+1).sample = annotation_tmp(i).sample_no + 1;
      event(end  ).type    =  'annotations';
      if ~isempty(annotation_tmp(i).annotationCategory)
        event(end  ).value    =  annotation_tmp(i).annotationCategory;
        %% 0:'undefined', 10:'epileptic', 20: 'others', 30:'noise', 40:'text'
      else
        event(end  ).value    =  99;
      end
    end
  end
  clear event_tmp;
  clear annotation_tmp;
  trigger_tmp = read_trigger(filename, 'header', hdr, 'denoise', false, 'chanindx', chanindx, 'detectflank', detectflank, 'threshold', threshold);
  trigger = [];
  for i = 1:length(trigger_tmp)
    trigger(end+1).sample = trigger_tmp(i).sample;
    trigger(end  ).value  = trigger_tmp(i).type;    % channel label
    trigger(end  ).type   = 'analogtrig';
  end
  clear trigger_tmp;
  % combine the triggers and the other events
  event = appendstruct(event, trigger); % search for "trigger" events according to 'trigchannel' defined outside the function
  if isfield(event, 'offset')
    event = rmfield(event,'offset');
  end
  if isfield(event, 'duration')
    event = rmfield(event,'duration');
  end
end

if isempty(event)
  ft_warning('no events were detected');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% this defines some usefull constants
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function handles = definehandles
handles.output = [];
handles.sqd_load_flag = false;
handles.mri_load_flag = false;
handles.NullChannel         = 0;
handles.MagnetoMeter        = 1;
handles.AxialGradioMeter    = 2;
handles.PlannerGradioMeter  = 3;
handles.RefferenceChannelMark = hex2dec('0100');
handles.RefferenceMagnetoMeter       = bitor( handles.RefferenceChannelMark, handles.MagnetoMeter );
handles.RefferenceAxialGradioMeter   = bitor( handles.RefferenceChannelMark, handles.AxialGradioMeter );
handles.RefferencePlannerGradioMeter = bitor( handles.RefferenceChannelMark, handles.PlannerGradioMeter );
handles.TriggerChannel      = -1;
handles.EegChannel          = -2;
handles.EcgChannel          = -3;
handles.EtcChannel          = -4;
handles.NonMegChannelNameLength = 32;
handles.DefaultMagnetometerSize       = (4.0/1000.0);       % Square of 4.0mm in length
handles.DefaultAxialGradioMeterSize   = (15.5/1000.0);      % Circle of 15.5mm in diameter
handles.DefaultPlannerGradioMeterSize = (12.0/1000.0);      % Square of 12.0mm in length
handles.AcqTypeContinuousRaw = 1;
handles.AcqTypeEvokedAve     = 2;
handles.AcqTypeEvokedRaw     = 3;
handles.sqd = [];
handles.sqd.selected_start  = [];
handles.sqd.selected_end    = [];
handles.sqd.axialgradiometer_ch_no      = [];
handles.sqd.axialgradiometer_ch_info    = [];
handles.sqd.axialgradiometer_data       = [];
handles.sqd.plannergradiometer_ch_no    = [];
handles.sqd.plannergradiometer_ch_info  = [];
handles.sqd.plannergradiometer_data     = [];
handles.sqd.eegchannel_ch_no   = [];
handles.sqd.eegchannel_data    = [];
handles.sqd.nullchannel_ch_no   = [];
handles.sqd.nullchannel_data    = [];
handles.sqd.selected_time       = [];
handles.sqd.sample_rate         = [];
handles.sqd.sample_count        = [];
handles.sqd.pretrigger_length   = [];
handles.sqd.matching_info   = [];
handles.sqd.source_info     = [];
handles.sqd.mri_info        = [];
handles.mri                 = [];
