# ----------------------------------------------------------------------------
# Copyright (c) 2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import importlib

from qiime2.plugin import Str, Plugin, Metadata, TypeMap, Visualization, Bool, Choices
from q2_types.sample_data import SampleData, AlphaDiversity
from q2_types.distance_matrix import DistanceMatrix

import q2_fmt
from q2_fmt import TSVFileFormat, ModelTests
from q2_fmt._engraftment import dataframe_adds_blank_column, group_timepoints
from q2_fmt._format import TSVFileDirFmt
from q2_fmt._visualizer import hello_world
from q2_fmt._type import GroupDist, Ordinal, Nominal

plugin = Plugin(name='fmt',
                version=q2_fmt.__version__,
                website='https://github.com/qiime2/q2-fmt',
                package='q2_diversity',
                description='This QIIME 2 plugin supports FMT analyses.',
                short_description='Plugin for analyzing FMT data.')

plugin.register_formats(TSVFileFormat, TSVFileDirFmt)
plugin.register_semantic_types(ModelTests, GroupDist, Ordinal, Nominal)
plugin.register_semantic_type_to_format(
    SampleData[ModelTests], TSVFileDirFmt, GroupDist[Ordinal | Nominal])

plugin.methods.register_function(
    function=dataframe_adds_blank_column,
    inputs={'dataframe': SampleData[ModelTests]},
    parameters={'column_name': Str},
    outputs=[('output_dataframe', SampleData[ModelTests])],
    input_descriptions={
        'dataframe': 'The original dataframe to be modified.'
    },
    parameter_descriptions={
        'column_name': 'The name of the blank column to be added to the dataframe.'
    },
    output_descriptions={
        'output_dataframe': 'The resulting dataframe.'
    },
    name='Modifies a dataframe with a specified blank column',
    description='This method adds a named blank column to an existing dataframe.'
)

plugin.methods.register_function(
    function=group_timepoints,
    inputs={'diversity_measure': DistanceMatrix | SampleData[AlphaDiversity] },
    parameters={'metadata': Metadata, 'time_column': Str,
                'reference_column': Str, 'subject_column': Str, 'control_column': Str},
    outputs=[('timepoint_dists', GroupDist[Ordinal]),
             ('reference_dists', GroupDist[Nominal])],
    parameter_descriptions={
        'metadata': 'The sample metadata.',
        'time_column': 'The column within the `metadata` that the `diversity_measure` should be grouped by.'
                       ' This column should contain simple integer values.',
        'control_column': 'The column within the `metadata` that contains any relevant control group IDs.'
                          ' Actual treatment samples should not contain any value within this column.',
        'reference_column': 'The column within the `metadata` that contains the sample to use as a reference'
                            ' for a given beta `diversity_measure`.'
                            ' For example, this may be the relevant donor sample to compare against.',
        'subject_column': 'The column within the `metadata` that contains the subject ID to be tracked against timepoints.',
    },
    output_descriptions={
        'timepoint_dists': 'The distributions for the `diversity_measure`, grouped by the selected `time_column`.'
                           ' May also contain subject IDs, if `subject_column` is provided in the `metadata`.',
        'reference_dists': ' When control is provided, this will be the control distribution (for Alpha Diversity)'
                           ' Or the pairwise control distances (for Beta Diversity).'
                        #    ' When control and reference are provided, this will be the distribution of the'
                        #    ' median distance from each control to all references.'
    },
)

plugin.visualizers.register_function(
    function=hello_world,
    inputs={},
    parameters={},
    input_descriptions={},
    parameter_descriptions={},
    name='Hello World Viz',
    description='Placeholder visualizer that outputs hello world.'
)

importlib.import_module('q2_fmt._transformer')
